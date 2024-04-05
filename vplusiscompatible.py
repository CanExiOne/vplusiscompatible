import mmap
import random
import string
import sys
import os.path
import shutil
from contextlib import redirect_stdout
import logging

github = "https://github.com/puszkapotato/vplusiscompatible"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)

print("Created by PuszkaPotato, download this software only from GitHub for safety reasons! " + github)

# Assign files from arguments to list
files = sys.argv[1:]

logging.info("Files to process: " + str(len(files)))

# Make a file backup
def make_backup(file):
      backup_dir = os.getcwd() + "\\backup\\"
      file_backup = backup_dir + os.path.basename(file) + "_backup"

      try:
            os.makedirs(backup_dir, exist_ok=True)
            if(os.path.isfile(file_backup)):
                  logging.info("A backup file already exists! Replacing file with new backup!")
                  os.remove(file_backup)
            else: 
                  logging.info(f"A copy of file has been made in: {file_backup}")

            shutil.copy(file, file_backup)

      except IOError as ioerror:
            logging.error("An error has occurred!" + ioerror)


# Generate random string with the same size/length as valheim_plus (12)
# It's random so people can't just add another incompatibility like "valheim_plud"
def get_random_string():
      letters = string.ascii_lowercase
      result = ''.join(random.choice(letters) for i in range(12))
      logging.info("Random string: " + result)
      return result

# Read file data and check if it has incompatibility with valheim_plus
def remove_incompatibility(file):
      try:
            with open(file, mode="r+", encoding="utf-8") as file_obj:
                  with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
                        file_data = mmap_obj.read()
                        check_incompatibility(file_data, mmap_obj, file)
      except:
            logging.error("An error has occurred while reading file or checking for incompatibility!")

# Check for incompatibility and remove if it exists
def check_incompatibility(file_data, mmap_obj, file):
      try:
            if b"valheim_plus" in file_data:
                        make_backup(file)
                        try:
                              file_new_data = file_data.replace(b"valheim_plus", get_random_string().encode())
                              mmap_obj[:] = file_new_data
                              mmap_obj.flush()
                              logging.info("Successfully removed V+ incompatibility in a mod " + os.path.basename(file))
                        except:
                              logging.critical(f"Couldn't remove incompatibility in the file! Contact this script developer at: {github}")
            else:
                  logging.error("File " + os.path.basename(file) + " doesn't have incompatibility with Valheim Plus!")

      except:
            logging.critical("An error has occurred!")

for file in files:
      if(os.path.isfile(file)):
            logging.info(f"Processing file {file}...")
            remove_incompatibility(file)
      else:
            logging.error(f"File {file} does not exist!")

if len(sys.argv) <= 1:
      logging.critical("Provide filename as an argument or drag&drop file on the script!")

print("All files processed! Press ENTER to close the program...")
input()