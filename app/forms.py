from django import forms
from .models import Post, Comment, Location


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'location', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': 'Enter post title', }),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Enter post text', }),
            'location': forms.Select(attrs={'class': 'form-control',
                                            'placeholder': 'Select a location'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Upload an image'}),

        }
        required = {
            'title': True,
            'content': True,
            'location': True,
            'image': False,
        }


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude', 'description']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['post', 'content']
        widgets = {
            'post': forms.Select(attrs={'class': 'form-control',
                                        'placeholder': 'Select post'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'placeholder': 'Enter comment'})
        }
        required = {
            'content': True
        }


