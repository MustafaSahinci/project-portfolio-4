from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from django import forms
from .models import Comment, Post, Category


choices = Category.objects.all().values_list('name' , 'name')
choice_list = []
for item in choices:
    choice_list.append(item)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'featured_image', 'excerpt', 'content')
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'category': forms.Select(choices= choice_list, attrs={"class": "form-control"}),
            'featured_image': forms.FileInput(attrs={"class": "form-control"}),
            'excerpt': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)

    # def clean_servings(self):
    #     """
    #     Ensures servings is greater than zero
    #     """
    #     value = self.cleaned_data.get("serves")
    #     print(value)
    #     if value < 1:
    #         raise forms.ValidationError(
    #             "The number of servings must be greater than zero"
    #             )
    #     return value
