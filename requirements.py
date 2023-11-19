import os
import platform
import subprocess

def install_package(package):
    try:
        subprocess.run(["pip3", "install", package])
    except subprocess.CalledProcessError as e:
        print(f"Error installing {package}: {e}")
        return False
    return True

def install_requirements():
    packages = ["socket", "scapy", "ipaddress"]

    for package in packages:
        install_package(package)
        clear_terminal()

def clear_terminal():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
install_requirements()
print("Installed requirements successfully.")
