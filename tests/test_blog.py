import unittest
from app.models import User, Blog
from app import db

class PitchModelTest(unittest.TestCase):
    """
    Test Case to test functionality of User Model
    """

    def setUp(self):
        """
        setUp method initializes all our objects before tests
        """
        self.new_user = User(username = "test_user", email = "testuser@mail.com", password = "testpass")
        self.new_blog = Blog(content = "Test Blog Content", user = self.new_user)

    def test_save_blog(self):
        """
        test_save_blog method to test if save method works
        """
        self.blog_save_id = self.new_blog.save()
        self.assertTrue(self.blog_save_id)

    def test_query_user_blogs(self):
        """
        test_save_blog method to test if get_user_blogs method works
        """
        self.blog_save_id = self.new_blog.save()
        self.query_output = Blog.get_user_blogs(self.blog_save_id)

        self.assertTrue(isinstance(self.query_output, list))
        self.assertTrue(all(isinstance(query_item, Blog) for query_item in self.query_output))
        
    def tearDown(self):
        """
        tearDown class to run after every test
        """
        db.session.delete(self.new_blog)
        db.session.delete(self.new_user)
        db.session.commit()