import os
import sys
import subprocess


def check_python_version():
    if not (sys.version_info.major == 3 and sys.version_info.minor == 7):
        print("Error: This script requires Python 3.7")
        sys.exit(1)


def find_requirements_files(path="."):
    requirements_files = []

    for root, dirs, files in os.walk(path):
        dirs[:] = [
            d for d in dirs if not d.startswith(".")
        ]  # Excluir directorios que comienzan con '.'

        for file in files:
            if file == "requirements.txt":
                requirements_files.append(os.path.join(root, file))

    return requirements_files


def install_requirements(requirements_file):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", requirements_file]
    )


def main():
    check_python_version()

    requirements_files = find_requirements_files()

    for req_file in requirements_files:
        print(f"Installing requirements from: {req_file}")
        install_requirements(req_file)


if __name__ == "__main__":
    main()
