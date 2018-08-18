from django.core.management.base import BaseCommand
from django.conf import settings
import os
# import pwd, grp

class Command(BaseCommand):
    help = "backs up the current sqllite db on an s3 bucket"
    def handle(self, *args, **options):
        # get database
        db_file = os.path.abspath(settings.DATABASES['default']['NAME'])
        sub_folder = os.path.dirname(db_file)
        # set file permissions
        os.chmod(db_file, 777)
        os.chmod(sub_folder, 777)
        # uid = pwd.getpwnam("www-data")[2]
        # gid = grp.getgrnam("www-data")[2]
        # os.chown(sub_folder, uid, gid)
