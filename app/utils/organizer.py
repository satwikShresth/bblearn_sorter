
import re
from datetime import datetime
from tabulate import tabulate
from pathlib import Path
from typing import List, Dict, Set
from zipfile import ZipFile


class Organizer:
    def __init__(self, target_path, group: Dict = {}, due_date=None):
        self.group: Dict = group
        self.target_path = target_path
        self.due_date = due_date
        self.late_submissions = []

    def organize(self):
        current_dir = Path(self.target_path)
        archive_dir = current_dir / 'archive'
        archive_dir.mkdir(exist_ok=True)

        for item in current_dir.iterdir():
            if item.is_file() and "gradebook" in item.stem and item.suffix == ".zip":
                with ZipFile(item, "r") as file:
                    file.extractall(current_dir)
                item.rename(archive_dir / item.name)

        for item in current_dir.iterdir():
            if item.is_dir() and "gradebook" in item.name:
                for file in item.iterdir():
                    target_file = current_dir / file.name
                    file.rename(target_file)
                item.rmdir()

        for filename in current_dir.iterdir():
            if filename.is_file():
                self.splitAndStore(filename.name, current_dir)

        for dirName in current_dir.iterdir():
            if dirName.is_dir() and dirName.name != 'archive':
                self.unzip_recursive(dirName)

        if self.due_date:
            self.check_late_submissions(current_dir)
            self.save_late_submissions_to_file()

        return 0

    def splitAndStore(self, filename: str, current_dir):
        userid_pattern = r'_([a-zA-Z]{2,5}\d{2,6})_'

        match = re.search(userid_pattern, filename)
        if match:
            userid = match.group(1)
            directory_name = userid
        else:
            print(f"No user ID found in filename '{filename}'. Skipping file.")
            return

        original_file_path = current_dir / filename

        if userid not in self.group:
            original_file_path.unlink(missing_ok=True)
            return

        if original_file_path.exists():
            directory_path = current_dir / directory_name

            if Path(filename).suffix == '.zip':
                directory_path /= "submission"

            directory_path.mkdir(exist_ok=True, parents=True)

            if Path(filename).suffix == '.txt':
                filename = 'submission.log'

            new_file_path = directory_path / filename
            original_file_path.rename(new_file_path)

            print(f"File '{filename}' stored in directory '{directory_name}'")
        else:
            print(f"File '{filename}' does not exist in the directory.")

    def unzip_recursive(self, dir_path):
        for item in dir_path.iterdir():
            if item.is_file() and item.suffix == '.zip':
                with ZipFile(item, 'r') as zip_ref:
                    zip_ref.extractall(dir_path)
                item.unlink()
        for subdir in dir_path.iterdir():
            if subdir.is_dir():
                self.unzip_recursive(subdir)

    def check_late_submissions(self, current_dir):
        submission_pattern = r"Date Submitted:\s+(.*)"
        date_format = "%A, %B %d, %Y %I:%M:%S %p"

        for student_dir in current_dir.iterdir():
            if student_dir.is_dir() and student_dir.name != "archive":
                submission_log = student_dir / "submission.log"
                if submission_log.exists():
                    with open(submission_log, "r") as f:
                        for line in f:
                            match = re.search(submission_pattern, line)
                            if match:
                                submission_date_str = match.group(1)
                                submission_date_str = submission_date_str.rsplit(' ', 1)[
                                    0]
                                submission_date = datetime.strptime(
                                    submission_date_str, date_format)
                                if submission_date > self.due_date:
                                    late_by = submission_date - self.due_date
                                    days, seconds = late_by.days, late_by.seconds
                                    hours = seconds // 3600
                                    minutes = (seconds % 3600) // 60

                                    late_by_str = f"{days} day{'s' if days != 1 else ''} and {
                                        hours} hour{'s' if hours != 1 else ''}"

                                    student_name = self.get_student_name_by_userid(
                                        student_dir.name)
                                    self.late_submissions.append(
                                        {
                                            "UserID": student_dir.name,
                                            "Name": student_name,
                                            "Late By": late_by_str,
                                            "Submitted": submission_date.strftime('%Y-%m-%d %H:%M:%S'),
                                            "Due Date": self.due_date.strftime('%Y-%m-%d %H:%M:%S')
                                        }
                                    )

    def get_student_name_by_userid(self, user_id):
        for student_user_id, student_name in self.group.items():
            if student_user_id == user_id:
                return student_name.Name
        return "Unknown"

    def save_late_submissions_to_file(self):
        table_data = [
            [student['UserID'], student['Name'], student['Late By'],
                student['Submitted'], student['Due Date']]
            for student in self.late_submissions
        ]

        table_str = tabulate(
            table_data, headers=["UserID", "Name", "Late By", "Submitted", "Due Date"], tablefmt="pretty"
        )

        with open(Path(self.target_path, "late_submissions.txt"), "w") as file:
            file.write(table_str)

        print("Late submissions written to late_submissions.txt")
