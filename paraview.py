import os
import requests
from bs4 import BeautifulSoup
import zipfile

def check_directory():
    directory_name = "Paraview"
    current_path = os.path.dirname(os.path.abspath(__file__))
    target_directory = os.path.join(current_path, directory_name)
    
    if os.path.exists(target_directory) and os.path.isdir(target_directory):
        print(f"The directory '{directory_name}' already exists.")
        return

    print(f"The directory '{directory_name}' does not exist. Fetching from the website...")
    url = "https://www.paraview.org/files/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    version_directories = soup.select('a[href^="v5."]')
    if not version_directories:
        print("No directories found on the website.")
        return

    print("Versions of Paraview on the website:")
    for i, directory in enumerate(version_directories):
        directory_name = directory.get("href")
        print(str(i) + ":", directory_name[1:-1])

    index = input("Choose one of the versions, we highly recommend 5.10 or above: ")
    choosen_version = version_directories[int(index)].get("href")[:-1]

    url = "https://www.paraview.org/files/" + choosen_version

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    zip_files = soup.select('a[href$=".zip"]')
    if not zip_files:
        print("No ZIP files found on the website.")
        return

    print("ZIP files on the website:")
    for i, file in enumerate(zip_files):
        file_name = file.get("href")
        print(str(i) + ":", file_name)

    index = input("Choose one of the versions, we highly recommend MIP: ")
    choosen_file = zip_files[int(index)].get("href")

    url = url + "/" + choosen_file
    download_file(url, current_path)

    zip_file_path = current_path + "/" + choosen_file
    extract_directory = current_path + "/Paraview"
    unzip_file(zip_file_path, extract_directory)

    # Write to version_control.txt
    version_control_path = os.path.join(current_path, "version_control.txt")
    with open(version_control_path, "w") as file:
        file.write(choosen_file[:-4] + "\n")
        file.write(choosen_version[1:])  # Replace with the desired number

    print(f"Version control file created: {version_control_path}")


def download_file(url, target_directory):
    filename = os.path.basename(url)
    file_path = os.path.join(target_directory, filename)

    print(f"Downloading file: {filename}")
    response = requests.get(url, stream=True)
    with open(file_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"File downloaded: {file_path}")


def unzip_file(zip_path, extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    print(f"ZIP file extracted to: {extract_dir}")

    # Delete the ZIP file
    os.remove(zip_path)
    print(f"ZIP file deleted: {zip_path}")


check_directory()