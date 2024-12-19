"""

Much credit goes to Chris Titus Tech for his Windows Utility, the backbone of this application and Talon as a whole.
https://github.com/ChrisTitusTech/winutil

"""

import os
import sys
import argparse
import subprocess

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def main():
    parser = argparse.ArgumentParser(description="Apply Talon profile using ChrisTitus' WinUtil.")
    parser.add_argument('--barebones', action='store_true', help='Use barebones.json')
    parser.add_argument('--gaming', action='store_true', help='Use gaming.json')
    parser.add_argument('--student', action='store_true', help='Use student.json')
    parser.add_argument('--professional', action='store_true', help='Use professional.json')
    parser.add_argument('--expert', action='store_true', help='Use expert.json')
    args = parser.parse_args()
    if not is_admin():
        print("Must be run as an administrator.")
        sys.exit(1)
    json_files = {
        'barebones': 'barebones.json',
        'gaming': 'gaming.json',
        'student': 'student.json',
        'professional': 'professional.json',
        'expert': 'expert.json'
    }
    selected_file = None
    for arg, file_name in json_files.items():
        if getattr(args, arg):
            selected_file = file_name
            break
    if not selected_file:
        print("No profile selected.")
        sys.exit(1)
    exe_dir = os.path.dirname(os.path.realpath(sys.executable))
    json_path = os.path.join(exe_dir, selected_file)
    if not os.path.exists(json_path):
        print(f"Invalid profile. Expected at: {json_path}")
        sys.exit(1)
    command = f"iex \"& {{ $(irm christitus.com/win) }} -Config '{json_path}' -Run\""
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        print("Profile has been applied.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply profile: {e.returncode}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
