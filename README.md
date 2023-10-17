# Application Requirements

**Summary**

A simple command line application used to manage a todo list.

## Installation

```sh
# Change directory into the directory where you want to install the application
cd /path/to/install/directory
# Clone the repository
git clone []
# Change directory into the repository
cd todo_cli
# Create a virtual environment. 
# This step is optional but recommended.
# This isolates the application from other Python applications on your system.
python3 -m venv venv
# Activate the virtual environment
# This enables the application to use the Python packages installed in the virtual environment.
source venv/bin/activate
# Install the application's dependencies
pip install -r requirements.txt

```

## Running the Application

```sh
# From the application's root directory, with the virtual environment activated...
# Run the application.
python3 todo.py [COMMAND] [OPTIONS]
# Omitting the command will display the help message.
python3 todo.py
```

## Running the Tests

```sh
# From the application's root directory, with the virtual environment activated...
# Run the tests.
pytest
```

## Deactivating the Virtual Environment

```sh
# From the application's root directory, with the virtual environment activated...
# Deactivate the virtual environment.
deactivate
```

## Application Details

Uses the following technologies:

- Python 3.11
- Click
  - Command line interface library
- SQLAlchemy 
  - ORM library
- SQLite 
  - Database
- pytest
  - Testing framework

**Features**

Add, update, list, mark as done/undone, and delete todo items.


**Data Model**

- Todo
  - id:             int         primary key
  - description:    string      not null
  - due_date:       datetime    not null
  - done:           boolean     not null
  

**Commands**

- add
  - description:    string
  - due_date:       datetime
  - done:           boolean

- list
    - done:         boolean

- update
  - id:             int
  - description:    string
  - due_date:       datetime
  - done:           boolean

- delete
    - id: int

- done
    - id: int

- undone
    - id: int