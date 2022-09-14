from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, Category, Comment, Profile


class TestViews(TestCase):
    """create the user, post, comment, category"""
    def setUp(self):
        test_user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.post = Post.objects.create(title='Test', author=test_user)
        self.comment = Comment.objects.create(
            body='Test-Comment', post=self.post
            )
        self.category = Category.objects.create(name='Test-Category')
        self.client.login(username="testuser", password="12345")
    
    """test home page """
    def test_get_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    """test post create page""" 
    def test_get_post_create_page(self):
        response = self.client.get('/post_create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_create.html')
    
    """test post edit page"""
    def test_get_post_edit_page(self):
        response = self.client.get('/edit/test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_edit.html')
    
    """test post delete page"""
    def test_get_post_delete_page(self):
        response = self.client.get('/delete/test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_delete.html')

    """test category page"""    
    def test_get_categories_page(self):
        response = self.client.get('/category/test-category')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'categories.html')

    """"test blog page""""
    def test_get_post_list_page(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog.html')
    
