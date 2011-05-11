__author__ = 'pauls'

from django import forms
from django.conf import settings
import datetime
from shutil import move
import os.path

from models import Upload
class UploadFileForm(forms.Form):
    file = forms.FileField()

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ['title']
