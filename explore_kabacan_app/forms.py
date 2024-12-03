from django import forms
from explore_kabacan_app.models import *
class CategoryForm(forms.ModelForm):
    pass

class TouristForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TouristForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tourist
        fields = '__all__'

class SpotForm(forms.ModelForm):
    pass
