from dataclasses import dataclass
from typing import List, Dict, Set


@dataclass
class Student:
    Name: str
    DrexelID: str
    UserID: str


@dataclass
class Group:
    Group: str
    TA: str
    Students: Dict[str, Student]


@dataclass
class Class:
    assignment_name: str
    groups: Dict[int, Group]

    def get_groups(self, group_numbers) -> Dict[str, Student]:
        requested_list = {}
        for group_number in group_numbers:
            requested_list |= self.groups[group_number].Students

        return requested_list


def parse_group_file(filename, ta_assignments, assignment_name):
    class_data = Class(
        assignment_name=assignment_name,
        groups={}
    )

    current_group = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if line.startswith("Group"):
                group_number = line.split()[-1]
                ta_name = ta_assignments.get(group_number, "Unknown TA")
                current_group = Group(Group=group_number,
                                      TA=ta_name, Students={})
                class_data.groups[group_number] = current_group
            elif line and current_group:
                parts = line.split()
                if len(parts) >= 3:
                    student = Student(
                        DrexelID=parts[0],
                        Name=" ".join(parts[1:-1]),
                        UserID=parts[-1]
                    )
                    current_group.Students[student.UserID] = student

    return class_data
