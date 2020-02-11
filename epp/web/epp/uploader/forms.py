from django import forms
from .models import *


class UploaderForm(forms.ModelForm):
    class Meta:
        model = Uploader
        fields = ['title', 'epp_image']




