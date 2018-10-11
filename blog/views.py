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

def prevpost_view(request, pk, tag):
    """
    returns the pk value of the post preceding the post given
    by the pk value
    """
    try:
        post = Post.objects.filter(pk=pk).select_related().get()
    except Post.DoesNotExist:
        raise Http404("Reference Post does not exist")
    try:
        prev_post = post.get_previous_by_pub_date()
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
        next_post = post.get_next_by_pub_date()
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

def get_other_post(post, post_type, tag):
    try:
        if   (post_type == 'first'):
            if (tag is not None):
                mypost = Post.objects.filter(tags__name=tag).order_by('pub_date').first().pk
            else:
                mypost = Post.objects.order_by('pub_date').first().pk
        elif (post_type == 'prev'):
            if (tag is not None):
                mypost = post.get_previous_by_pub_date(tags__name=tag).pk
            else:
                mypost = post.get_previous_by_pub_date().pk
        elif (post_type == 'next'):
            if (tag is not None):
                mypost = post.get_next_by_pub_date(tags__name=tag).pk
            else:
                mypost = post.get_next_by_pub_date().pk
        elif (post_type == 'latest'):
            if (tag is not None):
                mypost = Post.objects.filter(tags__name=tag).order_by('pub_date').last().pk
            else:
                mypost = Post.objects.order_by('pub_date').last().pk
        else:
            raise ValueError("type <%s> is not supported" % post_type)
    except Post.DoesNotExist:
        mypost = 0
    if(int(mypost) == int(post.pk)):
        mypost = 0
    url = reverse('post', kwargs={'pk': mypost})
    return (mypost, url)

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
    (prev_post, prev_url) = get_other_post(post, 'prev', None);
    # get next post
    (next_post, next_url) = get_other_post(post, 'next', None);
    # get first post
    (first_post, first_url) = get_other_post(post, 'first', None);
    # get latest post
    (last_post, last_url) = get_other_post(post, 'latest', None);

    # get tag links 
    tag_info = {}
    for mytag in post.tags.all():
        tag_links = {}
        # get previous tag_post
        (prev_tag_post, prev_tag_url) = get_other_post(post, 'prev', mytag.name);
        # get next tag_post
        (next_tag_post, next_tag_url) = get_other_post(post, 'next', mytag.name);
        # get first tag_post
        (first_tag_post, first_tag_url) = get_other_post(post, 'first', mytag.name);
        # get latest tag_post
        (last_tag_post, last_tag_url) = get_other_post(post, 'latest', mytag.name);

        tag_links['prev_post']  = prev_tag_post
        tag_links['prev_url']   = prev_tag_url
        tag_links['next_post']  = next_tag_post
        tag_links['next_url']   = next_tag_url
        tag_links['first_post'] = first_tag_post
        tag_links['first_url']  = first_tag_url
        tag_links['last_post']  = last_tag_post
        tag_links['last_url']   = last_tag_url
        tag_links['name']       = mytag.name.ljust(16)

        tag_info[mytag.name] = tag_links

    # render template
    return render(request, 'blog/post.html', context={
        'post'      : post,
        'first_post': first_post,
        'prev_post' : prev_post,
        'next_post' : next_post,
        'last_post' : last_post,
        'first_url' : first_url,
        'prev_url'  : prev_url,
        'next_url'  : next_url,
        'last_url'  : last_url,
        'tag_info'  : tag_info,
    })




