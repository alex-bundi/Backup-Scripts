import json
import smtplib
import os
import zipfile

def main():
    send_notification()

def send_notification():
    """ The purpose of the function is to access the backup directory,
        check the last zip archive added to backup zip files and use its information as the body 
        of the email it sends.
    """
    
    port = 465 # For SSL
    smtp_server = "smtp.gmail.com"
    
    # Get metadata
    with open("bak_creation_info.json", "r") as open_file:
        json_object = json.load(open_file)

    user = os.path.expanduser("~")
    ziparc_path = json_object["mail_details"].replace(os.path.expanduser("~"), "")
    latest_file = max(os.listdir(user + ziparc_path))
    added_file = os.path.join(user + ziparc_path, latest_file)
    
    with zipfile.ZipFile(added_file, mode="r") as archive:
        archive_info = archive.infolist()[-1]
        compressed_size = archive_info.compress_size
        original_size = archive_info.file_size

    message = f"""Hello there, 
    Backed up file name {latest_file}: 
        -> Location: {json_object["mail_details"]}, 
        -> Source:   {json_object["source"]}.
    It's details: Compressed size: {compressed_size} bytes
                  Original size: {original_size} bytes"""

    # Send mail
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(user= json_object["sender_email"], password= json_object["pwd"])
        server.sendmail(from_addr= json_object["sender_email"], to_addrs= json_object["receiver_email"], msg= message)

if __name__ == "__main__":
    main()