from django import forms
from explore_kabacan_app.models import *
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = ['username','password1','password2','email','first_name','last_name', 'is_active','is_staff','is_superuser']

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = SpotCategory
        fields = '__all__'

class TouristForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TouristForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tourist
        fields = '__all__'

class SpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpotForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Spot
        fields = '__all__'
