import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from loader.models import File, Feed

class FileTestCase(TestCase):
    def setUp(self):
        self.good_user = User.objects.create_user('good', 'good@example.com', 'password')
        self.bad_user = User.objects.create_user('bad', 'bad@example.com', 'password')

        self.usable_feed = Feed.objects.create(name='test_feed')
        self.usable_feed.members.add(self.good_user)

        self.usable_feed.save()
    # TODO: Ensure every file has a feed and a user
    # TODO: Delimiter can't be more than one.

    def test_needs_feed(self):
        with self.assertRaises(IntegrityError):
            File.objects.create()

    def test_needs_user(self):
        with self.assertRaises(IntegrityError):
            File.objects.create(feed=self.usable_feed)

    def test_authorised_user(self):
        f_good = File(feed=self.usable_feed, user=self.good_user)
        f_good.clean()
        with self.assertRaises(ValidationError):
            f_bad = File(feed=self.usable_feed, user=self.bad_user)
            f_bad.clean()

    def test_created_date(self):
        file = File.objects.create(feed=self.usable_feed, user=self.good_user)
        self.assertEqual(file.upload_date.date(), datetime.date.today())

    def test_file_path(self):
        pass

    def test_columns(self):
        file = File(user=self.good_user, feed=self.usable_feed, file_name='test.csv')

        self.assertEqual(file.get_columns(), [])

        file.set_columns(['1', '2', '3', '4', '5'])

        self.assertEqual(file.columns, '1,2,3,4,5')

        self.assertEqual(file.get_columns(), ['1','2','3','4','5'])

class FeedTestCase(TestCase):
    # TODO: Feeds cannot be accessed except by users in their users field.
    # TODO: They can only have unique names.
    # TODO: feed_directory_path returns an accurate path.
    pass
