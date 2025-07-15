from django import forms
from .models import InputImage

class ImageForm(forms.ModelForm):
    class Meta:
        model = InputImage
        fields = ("image",)