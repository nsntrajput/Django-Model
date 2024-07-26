from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import UploadedFile
from .models import DataFile

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(UploadFileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Upload'))

class SelectColumnsForm(forms.Form):
    columns = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    graph_type = forms.ChoiceField(choices=[('scatter3d', '3D Scatter Plot'), ('line3d', '3D Line Plot')])

    def __init__(self, *args, **kwargs):
        super(SelectColumnsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Select'))
class DataFileForm(forms.ModelForm):
    class Meta:
        model = DataFile
        fields = ['file']

