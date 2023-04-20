# Backup-Scripts

This repository contains a Python-based automatic backup system. It consists of three main files:
> 1. baksys.py: This file contains a class called CreateBackup, which creates backups of specified files and directories.
> 2. notification.py: This file contains a function called send_notification, which sends an email notification once the backup process is completed.
> 4. main.py: This file is the entry point for the system. It calls baksys.py and notification.py to create backups and send notifications, respectively.

## Dependencies

This system has the following dependencies:
1. tqdm: A Python library for creating progress bars.
2. smtplib: A Python library for sending email notifications.
3. zipfile: A Python library for working with zip files.

## How to Use

To use this system, follow these steps:
> 1. Clone this repository to your local machine.
> 2. Install the required dependencies using pip.
> 3. Open baksys.py and modify the bak_creation_info.json method to specify the files and directories you want to back up.
> 4. Open notification.py and modify the send_notification function to specify the email addresses and credentials for sending the notification.
> 5. Run main.py to start the backup process.
Note that you may need to run main.py as an administrator to avoid permission errors.

## Future Improvements

Some potential future improvements to this system include:
> - Give a user the capability to name the backup files.
> - Increase the speed of the execution of the scripts.
> - Adding more robust error handling and logging.
Automating:
> - Support for more backup storage options (e.g., cloud storage).
> - Support for more notification methods (e.g., SMS).
> - And lots more.

P.S. The scripts and their dependencies can be compiled into a .exe file to schedule the backups automatically.
