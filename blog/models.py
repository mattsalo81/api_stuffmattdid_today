from django.db import models
from rest_framework import serializers
from django.utils import timezone

# Create your models here.
class Attachment(models.Model):
    """
    An attachment is any file that can be attached to a blog post. These
    Files should be available to download, but not displayed/previewed, see
    ImageAttachment for display
    """
    upload = models.FileField(upload_to='blog_attachments')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.upload.name

class AttachmentSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateTimeField()
    class Meta:
        model = Attachment
        fields = '__all__'

class ImageAttachment(models.Model):
    """
    An Image Attachment is an attachment that is guaranteed to be an image.
    Blog posts should display any/all ImageAttachments
    """
    upload = models.ImageField(upload_to='blog_attachments')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.upload.name

class ImageAttachmentSerializer(serializers.ModelSerializer):
    upload_date = serializers.DateTimeField()
    class Meta:
        model = ImageAttachment
        fields = '__all__'

class Tag(models.Model):
    """
    A Tag is a word/short phrase that reflects the content of the
    post for the purposes of sorting
    """
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class TagSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=64)
    class Meta:
        model = Tag
        fields = '__all__'

class Post(models.Model):
    """
    A Post has a title, a body, a publication date, a collection of
    attachments, and a collection of images
    """
    title = models.CharField(max_length=128)
    body = models.TextField()
    pub_date = models.DateTimeField()
    files = models.ManyToManyField(Attachment, blank=True)
    images = models.ManyToManyField(ImageAttachment, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def is_posted_in_past(self):
        """Returns true if pub_date is in past/present, otherwise false"""
        now = timezone.now()
        return self.pub_date <= now


    def __str__(self):
        return self.title

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=128)
    body = serializers.CharField()
    pub_date = serializers.DateTimeField()
    files = AttachmentSerializer(many=True)
    images = ImageAttachmentSerializer(many=True)
    tags = TagSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'
        depth = 2
