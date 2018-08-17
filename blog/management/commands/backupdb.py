from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime
import boto3
import os

class Command(BaseCommand):
    help = "backs up the current sqllite db on an s3 bucket"
    def handle(self, *args, **options):
        # get database
        db_file = os.path.abspath(settings.DATABASES['default']['NAME'])
        file_name = os.path.basename(db_file)
        # get timestamp
        now = datetime.now()
        stamp = now.strftime('%Y_%m_%d__%H_%M_%S__%f')
        # make backup name
        folder = 'db_backups'
        backup_name = "%s/%s__%s" %(folder, file_name, stamp,)
        # upload to bucket
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        s3 = boto3.resource('s3')
        s3.Object(bucket, backup_name).put(Body=open(db_file, 'rb'))
