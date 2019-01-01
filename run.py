from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import sys
import configparser
import datetime


def get_parent_id(drive, root_id):
    now = datetime.datetime.now()
    now_date = now.strftime('%Y-%m-%d')

    file_list = drive.ListFile({
        'q': "title = '%s' and mimeType = 'application/vnd.google-apps.folder' and '%s' in parents" % (now_date, root_id)
    }).GetList()
    if len(file_list) > 0:
        return file_list[0]['id']

    parent_folder = drive.CreateFile({
        'title': now_date,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': root_id}]
    })
    parent_folder.Upload()
    return parent_folder['id']


def upload_file(drive, path, filename, parent_id):
    file = drive.CreateFile({'title': filename, 'parents': [{'id': parent_id}]})
    file.SetContentFile('%s/%s' % (path, filename))
    file.Upload()


gauth = GoogleAuth()
gauth.CommandLineAuth()

drive = GoogleDrive(gauth)

config = configparser.ConfigParser()
config.read('config.ini')
root_id = config['DEFAULT']['PARENT_FOLDER_ID']
parent_id = get_parent_id(drive, root_id)

for (path, dir, files) in os.walk('./backup_files/'):
    for filename in files:
        upload_file(drive, path, filename, parent_id)
