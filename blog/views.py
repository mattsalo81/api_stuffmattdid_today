from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command

# Create your views here.
def backupdb_view(request):
    """
    backs up the current db in an S3 bucket
    """
    call_command('backupdb')
    return HttpResponse("Database Backed up")
