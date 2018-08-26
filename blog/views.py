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

def latestpost_view(request):
    """
    gets the latest post, then calls post_view
    """
    try:
        post = Post.objects.order_by('pub_date', 'pk').latest('pub_date')
    except Post.DoesNotExist:
        raise Http404("Unable to find any posts")
    return post_view(request, post.pk)

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
    # get first post
    ordered = Post.objects.order_by('pub_date', 'pk')
    first_post = ordered.first().pk
    # get latest post
    last_post = ordered.last().pk
    # get links to posts
    first_url = reverse('post', kwargs={'pk': first_post})
    prev_url = reverse('post', kwargs={'pk': prev_post})
    next_url = reverse('post', kwargs={'pk': next_post})
    last_url = reverse('post', kwargs={'pk': last_post})
    # render template
    return render(request, 'blog/post.html', context={
        'post'      : post,
        'first_url' : first_url,
        'prev_url'  : prev_url,
        'next_url'  : next_url,
        'last_url'  : last_url,
    })




