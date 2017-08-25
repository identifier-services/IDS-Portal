from django import forms


class UploadForm(forms.Form):
    # new_investigation_type = forms.BooleanField(required=False)
    investigation_type = forms.CharField(max_length=50, required=False)
    # new_project = forms.BooleanField(required=False)
    project = forms.CharField(max_length=50,required=False )
    uploaded_file = forms.FileField(required=False)
