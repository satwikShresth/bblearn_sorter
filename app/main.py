#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path
from datetime import datetime
from utils.organizer import Organizer
from utils import parser


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Unzip and organize files in a directory, and process group assignments.'
    )
    parser.add_argument(
        'path',
        type=str,
        help='Path to the directory containing files to organize.'
    )
    parser.add_argument(
        '--group-file',
        '-g',
        type=str,
        help='Path to the group assignment text file.',
        required=True
    )
    parser.add_argument(
        '--ta-name',
        '-t',
        type=str,
        required=True,
        help='Name of the TA.'
    )
    parser.add_argument(
        '--groups',
        '-gr',
        type=str,
        required=True,
        help='Comma-separated group numbers to assign to the TA.'
    )
    parser.add_argument(
        '--assignment-name',
        '-a',
        type=str,
        required=True,
        help='Name of the assignment.'
    )
    parser.add_argument(
        '--due-date',
        '-d',
        type=lambda s: datetime.strptime(s, '%m/%d/%y'),
        help='Due date of the assignment in format: MM/DD/YY',
        required=True
    )
    parser.add_argument(
        '--organize',
        '-o',
        action='store_true',
        help='Organize the files. If not provided, the files will not be organized.'
    )

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    return args


def main(args):
    target_path = Path(args.path)
    group_nums = [s.strip() for s in args.groups.split(",")]

    if not target_path.exists():
        print(f"Error: The path '{args.path}' does not exist.")
        return 1

    ta_assignments = dict(
        map(lambda group: (group.strip(), args.ta_name),
            args.groups.split(","))
    )

    if not Path(args.group_file).exists():
        print(f"Error: The group file '{args.group_file}' does not exist.")
        return 1

    class_data = parser.parse_group_file(
        args.group_file, ta_assignments, args.assignment_name
    )

    organizer = Organizer(
        target_path, class_data.get_groups(group_nums), args.due_date)

    if args.organize:
        return organizer.organize()
    else:
        organizer.check_late_submissions(target_path)
        organizer.save_late_submissions_to_file()
        return 0


if __name__ == '__main__':
    sys.exit(main(parse_arguments()))
