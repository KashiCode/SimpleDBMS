# Database Management System
![Database](https://greencloudvps.com/greencloudvps/wp-content/uploads/2022/12/database-management-system-3-750x422.jpg)

## Introduction

This is a database management system built with [Python](https://www.python.org/), [PyQt5](https://pypi.org/project/PyQt5/), and [sqlite3](https://sqlite.org/index.html) that includes two user access levels: Admin and Employee. Employees can add, remove, and reduce stock items, track transactions, view database contents, and place orders. Admin users can manage user accounts. This program provides a fundamental model for learning stock management, application development, and simple SQL syntax.

## Updates
> v1.0.0 - First release of software. 

## Installation
- Clone the repository: git clone https://github.com/KashiCode/SimpleDBMS.git
- Ensure [Python](https://www.python.org/downloads/) and [sqlite3](https://www.sqlite.org/download.html) are installed on your system.
- Run directory.py to ensure the Python installation is on path. 
- Install dependencies: pip install -r requirements.txt
- Run config.py
- Run credentials.py
- Run launch.bat


## Dependencies
- Python 3
> This project requires Python 3.6 or later.
- PyQt5
> This project requires PyQt5 5.15.0 or later.
- sqlite3
> This project requires sqlite3 3.39.4 or later. 

## Usage

### First time launch
- When launching the program you must first modify the launch.bat file. 
1. Replace the Python directory path with the path to the directory. 
2. Replace the Python script path with the path to the python script.

```python
#Path to Python directory can be found using directory.py. 
@echo off
"Python Directory Path" "Python Script Path"
pause
```
### First time login

- Admin credentials: 
> Username: Admin

> Password: 1234

- Employee credentials
> Username: Employee

> Password: 1234

- To create your own credentials edit the c.execute statement in credentials.py:

```python
# Code to create your own login if the database does not feature the default credentials.
import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()

# Where username is your username, password is your password and role is either "employee" or "admin".
c.execute("INSERT INTO users VALUES ('username', 'password', 'role')")
conn.commit()

# Close the connection
conn.close()


```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://opensource.org/licenses/MIT)

## Contact
If you have any questions or comments, please feel free to contact me at ostrynskimaks@gmail.com



###### KashiCode © 2023
