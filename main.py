import baksys
import time
import notification
from tqdm import tqdm
import sys


def main():
    intiate_process()

def intiate_process() -> None:
    try: 
        for i in tqdm(range(1), desc="Processing", leave= True): # Progress bar
            start_process()
            final_process()
        print("Program finished executing.")
    except PermissionError:
        sys.exit("Locate auto_bak_sys.exe and run as administrator.")

    
    input("Press enter to exit.")
   
def start_process() -> None:
    """Call baksys.py script specifically the class CreateBackup to automate the backup process."""

    create_backup = baksys.CreateBackup()
    create_backup.create_bck_dir(dst_dir= create_backup.get_paths())
    create_backup.create_zip()

def final_process() -> None:
    notification.send_notification()


if __name__ == "__main__":
    main()