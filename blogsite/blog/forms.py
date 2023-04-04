from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin

from blog.models import Comment, Post

class PostForm(forms.ModelForm, LoginRequiredMixin):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            "title": forms.TextInput(attrs={'class': 'textinputclass'}),
            "text": forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['author'].initial = self.user

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.user:
            post.author = self.user
        if commit:
            post.save()

        return post


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            "author": forms.TextInput(attrs={'class': 'textinputclass'}),
            "text": forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }