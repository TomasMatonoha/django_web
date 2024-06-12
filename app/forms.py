from django import forms
from .models import Post, Location


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
                                            'placeholder': 'Select location', }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control',
                                                     'placeholder': 'Upload an image'}),

        }
        required = {
            'title': True,
            'content': True,
            'location': True,
            'image': False,
        }

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(PostForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['location'].queryset = Location.objects.all()
                self.user = user


class PostDeleteForm(forms.Form):
    posts = forms.ModelMultipleChoiceField(
        queryset=Post.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['posts'].queryset = Post.objects.filter(author=user)


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location name'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter longitude'}),
            'description': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Provide a description (optional)'}),
            'author': forms.HiddenInput(),
        }
        required = {
            'name': True,
            'latitude': True,
            'longitude': True,
            'description': False,
        }


class LocationDeleteForm(forms.Form):
    locations = forms.ModelMultipleChoiceField(
        queryset=Location.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['locations'].queryset = Location.objects.filter(author=user)
