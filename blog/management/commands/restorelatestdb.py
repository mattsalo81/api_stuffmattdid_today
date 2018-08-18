from django.core.management.base import BaseCommand
from django.conf import settings
import boto3
import botocore
import os

class Command(BaseCommand):
    help = "backs up the current sqllite db on an s3 bucket"
    def handle(self, *args, **options):
        # get database
        db_file = os.path.abspath(settings.DATABASES['default']['NAME'])
        file_name = os.path.basename(db_file)
        sub_folder = os.path.dirname(db_file)

        # prepare sub_folder
        try:
            os.mkdir(sub_folder)
        except OSError:
            raise

        # get bucket
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        s3 = boto3.resource('s3')
        subdir = "db_backups/%s" % (file_name,)
        bucket = s3.Bucket(bucket_name)

        # get last object in bucket
        objects = bucket.objects.filter(Prefix = subdir)
        sorted_objects = sorted(objects, key=lambda x: x.key, reverse=True)
        try:
            latest_key = sorted_objects[0].key
        except IndexError:
            print("No database backups found in S3 bucket <%s> directory <%subdir>" % (bucket_name, subdir,))

        # download
        try:
            bucket.download_file(latest_key, db_file)
            print("Downloaded <%s>" % latest_key)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("Could not download Backup!")
            else:
                raise

