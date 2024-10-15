
# Assignment Organizer and Group Processor

This project is a Python-based utility to organize and process student assignment submissions. It can assign groups to Teaching Assistants (TAs), check for late submissions based on a specified due date, and optionally organize files into group-specific directories.

## Features
- Organize assignment submissions by group.
- Automatically assign groups to TAs.
- Check for late submissions.
- Save late submissions report to a file.
  
## Prerequisites

Before you begin, ensure you have the following installed:
- pip
- [UV](https://docs.astral.sh/uv/#getting-started) (If you can directly insatll it)

## Installing Dependencies

To install dependencies, use the following command:

```bash
pip install uv # install uv using pip

uv sync
```

## Usage

The script is executed from the command line. Below is the usage format:

```bash
uv run -- \
python app/main.py <path_to_directory> \
--group-file <path_to_group_file> \
--ta-name <ta_name> \
--groups <group_numbers> \
--assignment-name <assignment_name> \
--due-date <due_date> \
--organize 
```

### Command-Line Arguments

| Argument                | Description                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| `<path_to_directory>`    | Path to the directory containing assignment files (required).                |
| `--group-file`, `-g`     | Path to the group assignment text file (required).                           |
| `--ta-name`, `-t`        | Name of the TA responsible for the listed groups (required).                 |
| `--groups`, `-gr`        | Comma-separated group numbers to assign to the TA (required).                |
| `--assignment-name`, `-a`| Name of the assignment (required).                                           |
| `--due-date`, `-d`       | Due date of the assignment in `MM/DD/YY` format (required).                  |
| `--organize`, `-o`       | Optional flag to organize the files into group-specific folders.             |

### Example Commands

1. **Organizing files and processing submissions:**

```bash

uv run -- \
python app/main.py /path/to/assignments \
--group-file /path/to/group_file.txt \
--ta-name "John Doe" \
--groups "1,2" \
--assignment-name "Assignment1" \
--due-date 10/01/24 \
--organize 
```

This will organize the assignment files into group directories and check for late submissions.

2. **Processing submissions without organizing:**

```bash
uv run -- \
python app/main.py /path/to/assignments \
--group-file /path/to/group_file.txt \
--ta-name "John Doe" \
--groups "1,2" \
--assignment-name "Assignment1" \
--due-date 10/01/24 \
--organize 
```

This will only check for late submissions and save the result to a file.

### Expected Output
- If `--organize` is passed, files will be organized into group-specific folders.
- Late submissions will be identified and saved in a report file.

### Error Handling
- If the specified path to the directory or group file does not exist, the script will display an error message and exit.

## Project Structure

```
/utils/
    organizer.py        # Handles file organization and late submission checks
    parser.py           # Parses group files and TA assignments
script.py                # Main script to run the program
README.md                # Documentation file
requirements.txt         # List of dependencies (if available)
```

## Additional Notes

- This project is built using the `Organizer` class and custom `parser` utility, which can be customized to fit specific needs.
- Ensure your input files are formatted correctly, especially the group assignment file.

## License

This project is open-source and free to use.
