#Author: Afonso Marques Mendes

from pathlib import Path
import time
import hashlib
import logging
import shutil
import argparse


#When comparing files, to ensure that they are different, it is useful to calculate their MD5 checksum and check if they are different.
#Note that the chance of two different files having the same MD5 checksum is extremely low, although not 0. But for our purposes, it is reliable and fast.

#The function get_MD5 computes the MD5 checksum for a file.

def get_MD5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""): #Reading in chunks is more efficient than reading the file as a whole, specially if the file is large
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


#Synchronize replica folder with source folder
def synchronize_folders(source_folder, replica_folder, log_file):

    #Walking through the source folder
    for root, dirs, files in Path(source_folder).walk():
        relative_path = Path(root).relative_to(source_folder)
        replica_root = replica_folder / relative_path

        for dir_name in dirs:
            #source_dir = root / dir_name #################    PRECISO DESTA LINHA?? ACHO QUE NÃO    #####################
            replica_dir = replica_root / dir_name

            #If a directory does not exist in the replica folder, create it
            if not Path(replica_dir).exists():
                Path(replica_dir).mkdir()
                logging.info(f"Directory created : {replica_dir}")
                print(f"Directory created : {replica_dir}")

        for file_name in files:
            source_file = root / file_name
            replica_file = replica_root / file_name

            #Copying the files to the replica directory
            if not Path(replica_file).exists() or get_MD5(source_file) != get_MD5(replica_file):
                shutil.copy2(source_file, replica_file)
                logging.info(f"File copied : {replica_file}")
                print(f"File copied : {replica_file}")

    #Removing files and directories in replica folder that are not in source
    for root, dirs, files in Path(replica_folder).walk():
        relative_path = Path(root).relative_to(replica_folder)
        source_root = Path(source_folder) / relative_path
        
        for file_name in files:
            replica_file = Path(root) / file_name
            source_file = source_root / file_name
        
            # Removing files in replica folder
            if not source_file.exists():
                replica_file.unlink()
                logging.info(f"File removed: {replica_file}")
                print(f"File removed: {replica_file}")
        
        for dir_name in dirs:
            replica_dir = Path(root) / dir_name
            source_dir = source_root / dir_name
        
            # Removing directories in replica folder
            if not source_dir.exists():
                shutil.rmtree(replica_dir)
                logging.info(f"Directory removed: {replica_dir}")
                print(f"Directory removed: {replica_dir}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help = "Path to the Source Folder")
    parser.add_argument("replica", help = "Path to the Replica Folder")
    parser.add_argument("interval", type = int, help = "Time Interval for synchronization, in seconds")
    parser.add_argument("log", help = "Path to the Log File")
    args = parser.parse_args()

    source_folder = args.source
    replica_folder = args.replica
    interval = args.interval
    log_file = args.log

    #Create the log file
    Path(log_file).touch()

    #Set up logging
    logging.basicConfig(
        filename = log_file,
        encoding = "utf-8",
        level = logging.INFO,
        format = "{asctime} - {levelname} - {message}",
        style = '{',
        force=True      
        )

    #If source folder does not exist, display the error and stop running
    if not Path(source_folder).exists:
        print(f"ERROR: Source folder {source_folder} does not exist")
        return

    #If replica folder does not exist, create it
    if not Path(replica_folder).exists:
        Path(replica_folder).mkdir()
        logging.info(f"Replica Folder {replica_folder} created")
        print(f"Replica Folder {replica_folder} created")

    current_time = time.strftime("%H:%M:%S")
    logging.info(f"Synchronization started at {current_time} every {interval} seconds")

    while True:
        synchronize_folders(source_folder, replica_folder, log_file)
        time.sleep(interval)


if __name__ == "__main__":
    main()
