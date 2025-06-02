from django import forms

from .models import *

class modelform(forms.ModelForm):
    class Meta:
        model = user
        # fields = '__all__'
        exclude = ['uname', 'pswd']

class teacherform(forms.ModelForm):
    class Meta:
        model = tutor
        exclude = ['uname', 'pswd','address','qualification','lang','course','action']
