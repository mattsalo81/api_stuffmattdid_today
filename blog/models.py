from django.db import models

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

class ImageAttachment(models.Model):
    """
    An Image Attachment is an attachment that is guaranteed to be an image.
    Blog posts should display any/all ImageAttachments
    """
    upload = models.ImageField(upload_to='blog_attachments')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.upload.name

class Tags(models.Model):
    """
    A Tag is a word/short phrase that reflects the content of the
    post for the purposes of sorting
    """
    name = models.CharField(max_length=64)

class Post(models.Model):
    """
    A Post has a title, a body, a publication date, a collection of
    attachments, and a collection of images
    """
    title = models.CharField(max_length=128)
    body = models.TextField()
    pub_date = models.DateTimeField()
    files = models.ManyToManyField(Attachment)
    images = models.ManyToManyField(ImageAttachment)
    tags = models.ManyToManyField(Tags)
