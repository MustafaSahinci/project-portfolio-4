from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from django import forms
from .models import Comment, Post, Category, Profile

"""add created categorys to the list"""
choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)


class CommentForm(forms.ModelForm):
    """creates the comment form on post details and comment edit"""
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(attrs={"class": "form-control"}),
        }


class ProfileForm(forms.ModelForm):
    """creates the Profile form on Profile create page"""
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'profile_image', 'bio',
                  'facebook_url', 'instagram_url', 'twitter_url',
                  'linkedin_url', 'github_url',)
        widgets = {
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'profile_image': forms.FileInput(attrs={"class": "form-control"}),
            'bio': forms.Textarea(attrs={"class": "form-control"}),
            'facebook_url': forms.TextInput(attrs={"class": "form-control"}),
            'instagram_url': forms.TextInput(attrs={"class": "form-control"}),
            'twitter_url': forms.TextInput(attrs={"class": "form-control"}),
            'linkedin_url': forms.TextInput(attrs={"class": "form-control"}),
            'github_url': forms.TextInput(attrs={"class": "form-control"}),
        }


class PostForm(forms.ModelForm):
    """Creates the post form for post create and post edit"""
    class Meta:
        model = Post
        fields = ('title', 'excerpt', 'category', 'featured_image', 'content')
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'category': forms.Select(
                choices=choice_list, attrs={"class": "form-control"}),
            'featured_image': forms.FileInput(attrs={"class": "form-control"}),
            'excerpt': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
