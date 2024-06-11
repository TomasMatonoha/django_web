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


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'latitude', 'longitude', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location name'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter longitude'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Provide a description (optional)'}),
            'author': forms.HiddenInput(),
        }
        required = {
            'name': True,
            'latitude': True,
            'longitude': True,
            'description': False,
        }


class LocationDeleteForm(forms.Form):
    location_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean_location_id(self):
        location_id = self.cleaned_data['location_id']
        if not Location.objects.filter(pk=location_id).exists():
            raise forms.ValidationError("Invalid location.")
        return location_id
