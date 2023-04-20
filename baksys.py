import os
import json
import sys
import zipfile
from zipfile import ZIP_DEFLATED
import time

class ZipArchives:
    """ This class provides a manual way of accessing all of the functionality of the whole script.
        The functionality includes creating a backup, searching the archives already created, displaying 
        and extracting according to the search criteria. 
    """
    
    def __init__(self, instructions):
        self.instructions = instructions

         
    def get_instructions(self) -> None:
        """ Gets instructions from the console and executes as per the specified instructions."""

        create_backup = CreateBackup()
        self.bak_dir = create_backup.create_bck_dir(dst_dir= create_backup.get_paths())

        if self.instructions == "Create":
            self.bak_dir
            create_backup.create_zip()
        elif self.instructions == "Display Content":
            self.display_zip_files(bak_zips= self.bak_dir[0])
        elif self.instructions == "Extract":
            self.extract_files(zips_bck= self.bak_dir[0], ext_files= self.bak_dir[1]) 

    def search_archives(self) -> str:
        """ Specify search criteria. """

        self.count = 10 # Date length characters
        while True:
            self.search_date = input("search: ")
            if len(self.search_date) == self.count and self.search_date[4] == "/" and self.search_date[7] == "/":
                return self.search_date
            else:
                self.search_date
                print("Required format: yy/mm/dd = 2023/03/09")

    def display_zip_files(self, bak_zips) -> None:
        """ Display specified zip archive."""
        
        self.bak_zips = bak_zips
        self.specified_date = self.search_archives()
        self.found_zips = []

        for current_archives in os.listdir(self.bak_zips):
            self.lst_underscore = current_archives.rindex("_")
            self.date = current_archives[self.lst_underscore + 1:] # Gets timestamp
            if self.date[:4] == self.specified_date[:4] and self.date[4:6] == self.specified_date[5:7] and self.date[6:8] == self.specified_date[-2:]:
                self.found_zips.append(current_archives)
                with zipfile.ZipFile(os.path.join(self.bak_zips, current_archives), "r") as archive: # To avoid FileNotFoundError
                    print(current_archives)
                    archive.printdir()
        print(f"Zipfiles displayed: {len(self.found_zips)}")

    def extract_files(self, zips_bck, ext_files) -> None:
        """ Unzip the compressed zip archive to a folder.
        
            Args:
                zips_bck: path to backed up zip files directory
                ext_files: path to extracted zip file directory
        """

        self.zips_bck = zips_bck
        self.ext_files = ext_files
        self.specified_date = self.search_archives()

        for all_zips in os.listdir(self.zips_bck):
            self.lst_underscore = all_zips.rindex("_")
            self.date = all_zips[self.lst_underscore + 1:]
            if self.date[:4] == self.specified_date[:4] and self.date[4:6] == self.specified_date[5:7] and self.date[6:8] == self.specified_date[-2:]:
                with zipfile.ZipFile(os.path.join(self.zips_bck, all_zips), mode="r") as archive:
                    archive.extractall(self.ext_files)


class CreateBackup:
    """ The class's main functionality is to get the paths for the source of files and 
        their destination from a config file in a JSON format, it creates directories 
        for storing and extracting the zip files.
        
        The last functionality then walks the source directory, 
        compresses all the folders and files and then moves
        them to the specified destination.

        P.S. The class can be automated and can be used to create a .exe file which can then be scheduled
    """
    user = os.path.expanduser("~")

    def get_paths(self) -> tuple:
        """ Reads from the JSON file the source of files and destination."""
        try:
            with open("bak_creation_info.json", "r") as open_file:
                self.json_object = json.load(open_file)
        except json.decoder.JSONDecodeError:
            raise ValueError("Invalid \escape character in one of the paths: line 2 column 25 (char 26)")

        self.src_system_user_path = self.json_object["source"].replace(self.user, "") 
        self.dst_system_user_path = self.json_object["destination"].replace(self.user, "") 

        if os.path.exists(self.user + self.src_system_user_path) == True and os.path.exists(self.user + self.dst_system_user_path) == True:
            self.needed_paths = []
            self.src_file_path = self.user + self.src_system_user_path
            self.needed_paths.append(self.src_file_path)
            self.dst_file_path = self.user + self.dst_system_user_path
            self.needed_paths.append(self.dst_file_path)
            return self.needed_paths
        else:
            sys.exit("One of the paths(source or destination) in bak_creation_info.json is invalid or doesn't exist.")

    def create_bck_dir(self, dst_dir) -> tuple:
        """ Creates the directory to store the zip files and extracted zip files.

            Args:
                dst_dir: path to create the main directory and its subfolders
        """

        self.dst_dir = dst_dir
        self.backup_dir = os.path.join(self.dst_dir[1], "backup directory")
        self.backup_zipfiles = os.path.join(self.backup_dir, "backup zipfiles")
        self.backup_files = os.path.join(self.backup_dir, "backup files")

        if not os.path.exists(self.backup_dir): # Check if folder exists
            os.makedirs(self.backup_zipfiles)
            os.makedirs(self.backup_files)
        return self.backup_zipfiles, self.backup_files
    
    @staticmethod
    def get_timestamp() -> str:
        return time.strftime("%Y%m%d-%H%M%S")

    def create_zip(self) -> None:
        """ Create zip and save to destination of all zip archives.
            
            Args:
                timestr: system date and time stamp
        """
        self.timestr = self.get_timestamp()
        self.get_paths()
        
        if len(os.listdir(self.user + self.src_system_user_path)) > 0:
            zip_file_path = os.path.join(self.backup_zipfiles, f"BAK_scripts_files_{self.timestr}.zip") # Create zipfile in destination with a hard-coded name
            with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED, compresslevel= 6) as archive:
                for root, dirs, files in os.walk(self.user + self.src_system_user_path): # Iterate over all the files and directories
                    for file_name in files: # Add each file to the zip
                        file_path = os.path.join(root, file_name)
                        archive.write(file_path, os.path.relpath(file_path, self.user + self.src_system_user_path)) # To preserve directory structure
        else:
            sys.exit(f"There are no files to backup in source directory\n\t-> {self.json_object['source']}")


def main():
    zip_archives = ZipArchives(instructions= input("What do you want to do?\n\t Options: Create, Display Content, Extract\n").title())
    zip_archives.get_instructions()
    
    
if __name__ == "__main__":
    main()