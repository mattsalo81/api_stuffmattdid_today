from django.test import TestCase
from blog import models, views
from datetime import datetime, timedelta
from django.utils import timezone
from django.test import Client
from django.core.urlresolvers import reverse
import json

# Create your tests here.

class PostTestCases(TestCase):
    def set_up_reference_posts(self):
        tag1 = models.Tag(name="Winemaking");
        tag2 = models.Tag(name="Embedded");
        tag1.save()
        tag2.save()

        date1 = datetime.now(tz=timezone.utc)
        delta = timedelta(days=1)
        date2 = date1 - delta

        post1 = models.Post(
            title='Test Post about Wine',
            body="""I'm not an alcoholic""",
            pub_date=date1
        )
        post1.save()
        post1.tags.add(tag1.pk)
        post1.save()

        post2 = models.Post(
            title='Test Post about embedded control',
            body="""I sure do love reading manuals""",
            pub_date=date2
        )
        post2.save()
        post2.tags.add(tag2.pk)
        post2.save()


    def test_pk(self):
        """checks if the blog posts exist with 1/2 pk"""
        self.set_up_reference_posts()
        post = models.Post.objects.get(pk=1)
        self.assertEqual(post.title, 'Test Post about Wine')
        post = models.Post.objects.get(pk=2)
        self.assertEqual(post.title, 'Test Post about embedded control')

    def test_singlepost_view(self):
        """
        queries a single known pk, checks for known fields
        (no attachment checking).  Queries a PK that does not exist
        and checks for 404
        """
        self.set_up_reference_posts()
        client = Client()
        response = client.get(reverse('singlepost', kwargs={'pk': 1}))
        data = json.loads(response.content)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Post about Wine')
        self.assertEqual(data['body'], "I'm not an alcoholic")
        self.assertEqual(data['tags'][0]['name'], 'Winemaking')
        response = client.get(reverse('singlepost', kwargs={'pk': 0}))
        self.assertEqual(response.status_code, 404)
       
    def test_nextpost_view(self):
        """
        queries a single known pk, checks that pk of next post is
        correct (test case queries are uploaded in reverse order of date)
        then checks for proper 404s
        """
        self.set_up_reference_posts()
        client = Client()
        response = client.get(reverse('nextpost', kwargs={'pk': 2}))
        self.assertEqual(response.content, b'1')
        response = client.get(reverse('nextpost', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('nextpost', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 404)
       
    def test_prevpost_view(self):
        """
        queries a single known pk, checks that pk of previous post is
        correct (test case queries are uploaded in reverse order of date)
        then checks for proper 404s
        """
        self.set_up_reference_posts()
        client = Client()
        response = client.get(reverse('prevpost', kwargs={'pk': 1}))
        self.assertEqual(response.content, b'2')
        response = client.get(reverse('prevpost', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        response = client.get(reverse('prevpost', kwargs={'pk': 3}))
        self.assertEqual(response.status_code, 404)

    def test_is_past(self):
        """
        Creates a record in the past/future and checks that each can
        be identified as such
        """
        self.set_up_reference_posts()
        post = models.Post.objects.get(pk=2)
        self.assertTrue(post.is_posted_in_past())
        tomorrow = timezone.now() + timedelta(days=1)
        post.pub_date = tomorrow
        self.assertFalse(post.is_posted_in_past())
        

