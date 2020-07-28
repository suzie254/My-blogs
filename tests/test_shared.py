import unittest
from app.models import User, Blog, Comment
from app import db

class SharedModelTest(unittest.TestCase):
    """
    Test Case to test functionality of User Model
    """

    def setUp(self):
        """
        setUp method initializes all our objects before tests
        """
        self.new_user = User(username = "test_user", email = "testuser@mail.com", password = "testpass")
        self.new_blog = Blog(content = "Test Blog Content", user_id = self.new_user.id)
        self.new_comment = Comment(content = "very belivable comment", blog_id = self.new_blog.id, user_id = self.new_user.id)

    def test_user_instance(self):
        """
        test_instance test case to test if new_user is of instance User
        """
        self.assertTrue(isinstance(self.new_user, User))

    def test_blog_instance(self):
        """
        test_instance test case to test if new_blog is of instance Blog
        """
        self.assertTrue(isinstance(self.new_blog, Blog))

    def test_comment_instance(self):
        """
        test_instance test case to test if new_comment is of instance Comment
        """
        self.assertTrue(isinstance(self.new_comment, Comment))
    