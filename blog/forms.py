from django_summernote.widgets import SummernoteInplaceWidget, SummernoteWidget
from django import forms
from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'featured_image', 'excerpt', 'content')
        widgets = {
            'content': SummernoteWidget(),
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
