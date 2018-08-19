from django.shortcuts import render
from django.http import HttpResponse
from django.core.management import call_command
from django.shortcuts import get_object_or_404

# Create your views here.
def backupdb_view(request):
    """
    backs up the current db in an S3 bucket
    """
    call_command('backupdb')
    return HttpResponse("Database Backed up")

def singlepost_view(request):
    """
    displays the post given by the pk value
    """
    post = get_object_or_404(Post, pk=pk)
    return HttpResponse("Got the post \"" + post + '"')
