"""

Much credit to Chris Titus Tech's Windows Utility, which provides the backbone for this process:
https://github.com/ChrisTitusTech/winutil

"""

import os
import sys
import argparse
import subprocess
import requests

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def download_json(profile_name, destination_path):
    base_url = "https://raw.githubusercontent.com/ravendevteam/talon-applyprofile/refs/heads/main/profiles/"
    json_url = f"{base_url}{profile_name}.json"
    try:
        print(f"Downloading {profile_name}.json from {json_url}...")
        response = requests.get(json_url, timeout=10)
        response.raise_for_status()
        with open(destination_path, "wb") as json_file:
            json_file.write(response.content)
        print(f"Downloaded {profile_name}.json to {destination_path}.")
    except requests.RequestException as e:
        print(f"Failed to download {profile_name}.json: {e}")
        sys.exit(1)

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
        'barebones': 'barebones',
        'gaming': 'gaming',
        'student': 'student',
        'professional': 'professional',
        'expert': 'expert'
    }
    selected_profile = None
    for arg, profile_name in json_files.items():
        if getattr(args, arg):
            selected_profile = profile_name
            break
    if not selected_profile:
        print("No profile selected.")
        sys.exit(1)
    exe_dir = os.path.dirname(os.path.realpath(sys.executable))
    json_path = os.path.join(exe_dir, f"{selected_profile}.json")
    download_json(selected_profile, json_path)
    command = f"iex \"& {{ $(irm christitus.com/win) }} -Config '{json_path}' -Run\""
    try:
        subprocess.run(["powershell", "-Command", command], check=True)
        print("Profile has been applied.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to apply profile: {e.returncode}.")
        sys.exit(1)

if __name__ == "__main__":
    main()
