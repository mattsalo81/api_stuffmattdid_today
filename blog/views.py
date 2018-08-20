from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.management import call_command
from django.core import serializers
from .models import Post, PostSerializer
from rest_framework.renderers import JSONRenderer

# Create your views here.
def backupdb_view(request):
    """
    backs up the current db in an S3 bucket
    """
    call_command('backupdb')
    return HttpResponse("Database Backed up")

def singlepost_view(request, pk):
    """
    displays the post given by the pk value
    """
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    serializer = PostSerializer(post)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content)
