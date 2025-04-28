from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    query = forms.CharField(widget=forms.Textarea, label='Enter your cleaning query:')
