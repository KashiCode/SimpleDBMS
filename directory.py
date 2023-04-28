import subprocess
import sys

def is_python_on_path():
    try:
        subprocess.check_output(['python', '--version'])
        return True
    except subprocess.CalledProcessError:
        return False

if is_python_on_path():
    print("Python is on the system's path")
    print("Python is installed in:", sys.executable)
else:
    print("Python is NOT on the system's path")
   
