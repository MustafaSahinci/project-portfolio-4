from .models import Comment, Post
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_image', 'excerpt', 'content')
    
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)

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
