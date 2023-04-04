from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from blog.models import Comment, Post

# Customise a widget
class AuthorWidget(forms.Widget):
    input_type = 'text'

    def __init__(self, user=None, attrs=None):
        self.user = user
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if self.user:
            value = self.user.username
        else:
            value = ''

        final_attrs = self.build_attrs(attrs)
        final_attrs['name'] = name
        final_attrs['type'] = 'text'
        final_attrs['value'] = value
        final_attrs['readonly'] = 'readonly'
        return mark_safe(f'<input{flatatt(final_attrs)} />')


class AuthorInputForm(forms.ModelForm, LoginRequiredMixin):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['author'].initial = f'{self.user.username} ({self.user.email})'
            self.fields['author'].widget = AuthorWidget(user=self.user)

    def save(self, commit=True):
        post = super().save(commit=False)
        if self.user:
            post.author = self.user
        if commit:
            post.save()

        return post


class PostForm(AuthorInputForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            "title": forms.TextInput(attrs={'class': 'textinputclass'}),
            "text": forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }


class CommentForm(AuthorInputForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            "author": forms.TextInput(attrs={'class': 'textinputclass'}),
            "text": forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }