import os
import shutil
from datetime import datetime
from config import BACKUP_PATH, DATABASE_PATH
from flask import current_app


def restore_from_backup(backup_name):
    original_db_path = os.path.join(DATABASE_PATH, current_app.config['DB_NAME'])
    backup_db_path = os.path.join(BACKUP_PATH, backup_name)
    shutil.copy(backup_db_path, original_db_path)

def get_backups_info():
    backup_info_list = []
    for backup_name in os.listdir(BACKUP_PATH):
        backup_path = os.path.join(BACKUP_PATH, backup_name)

        if os.path.isfile(backup_path):
            backup_size_bytes = os.path.getsize(backup_path)
            backup_size_mb =  backup_size_bytes / (1024 * 1024)  # Convert bytes to gigabytes
            backup_creation_time = datetime.fromtimestamp(os.path.getctime(backup_path))

            backup_info_list.append({
                'name': backup_name,
                'size': "{:.2f} MB".format(backup_size_mb),
                'creation_time': backup_creation_time,
                'is_createble': True,
                'is_deletable': True,
                'is_reviewed': True,
                'is_editable': False,
            })

    return backup_info_list


def create_backup():
    timestamp = datetime.now().strftime('%Y%m%d%H%M')
    backup_name = f'backup_{timestamp}.sqlite'
    backup_path = os.path.join(BACKUP_PATH, backup_name)
    original_db_path = os.path.join(DATABASE_PATH, current_app.config['DB_NAME'])

    shutil.copy(original_db_path, backup_path)
    return backup_path

def delete_backup(backup_name):
    backup_path = os.path.join(BACKUP_PATH, backup_name)
    
    if os.path.exists(backup_path):
        os.remove(backup_path)
        return True
    else:
        return False
