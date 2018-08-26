from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.core.management import call_command
from django.core import serializers
from .models import Post, PostSerializer
from rest_framework.renderers import JSONRenderer
from django.core.urlresolvers import reverse

# Create your views here.
def backupdb_view(request):
    """
    backs up the current db in an S3 bucket
    """
    call_command('backupdb')
    return HttpResponse("Database Backed up")

def jsonpost_view(request, pk):
    """
    returns JSON formatted post given by the pk value
    """
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    serializer = PostSerializer(post)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content)

def prevpost_view(request, pk):
    """
    returns the pk value of the post preceding the post given
    by the pk value
    """
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Reference Post does not exist")
    try:
        prev_post = post.get_previous_by_pub_date();
    except Post.DoesNotExist:
        raise Http404("Previous Post does not exist")
    return HttpResponse(prev_post.pk)

def nextpost_view(request, pk):
    """
    returns the pk value of the post following the post given
    by the pk value
    """
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Reference Post does not exist")
    try:
        next_post = post.get_next_by_pub_date();
    except Post.DoesNotExist:
        raise Http404("Next Post does not exist")
    return HttpResponse(next_post.pk)

def post_view(request, pk):
    """
    Displays the contents of a blog post, given by the primary key
    """
    # get current post
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    # get previous post
    try:
        prev_post = post.get_previous_by_pub_date().pk;
    except Post.DoesNotExist:
        prev_post = pk;
    # get next post
    try:
        next_post = post.get_next_by_pub_date().pk;
    except Post.DoesNotExist:
        next_post = pk;
    # get links to next/prev posts
    prev_url = reverse('post', kwargs={'pk': prev_post})
    next_url = reverse('post', kwargs={'pk': next_post})
    # render template
    return render(request, 'blog/post.html', context={
        'post'      : post,
        'next_url'  : next_url,
        'prev_url'  : prev_url,
    })




