from django import forms
from explore_kabacan_app.models import *
from django.contrib.auth.forms import UserCreationForm


class PersonelTouristForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonelTouristForm, self).__init__(*args, **kwargs)

        if 'dob' in self.fields:
            self.fields['dob'].label = 'Birth Date'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            field.widget.is_required = True

    class Meta:
        model = Tourist
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput({'type': 'date'}),
        }
        exclude = ('destination',)


class CreateTouristForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CreateTouristForm, self).__init__(*args, **kwargs)

        if 'dob' in self.fields:
            self.fields['dob'].label = 'Birth Date'

        if 'middlename' in self.fields:
            self.fields['middlename'].label = 'Middle (Optional)'

        if 'gender' in self.fields:
            self.fields['gender'].choices = [('Male', 'Male'), ('Female', 'Female')]
            self.fields['gender'].label = 'Gender'
        
        if 'destination' in self.fields:
            self.fields['destination'] = forms.ModelChoiceField(
                queryset=Spot.objects.all(),
                empty_label=None,
                widget=forms.Select(attrs={'class': 'form-control'})
            )
            self.fields['destination'].label = 'Destination'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control', 'placeholder': field_name  })

    class Meta:
        model = Tourist
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput({'type': 'date'}),
        }


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['first_name'].label = 'Firstname'
        self.fields['last_name'].label = 'Lastname'
        self.fields['email'].label = 'Email Address'
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Confrim Password'
        self.fields['assigned_to'].label = 'Designation Tourist Spot'
        self.fields['assigned_to'] = forms.ModelChoiceField(
            queryset=Spot.objects.all(),
            empty_label=None,
            widget=forms.Select(attrs={'class': 'form-control'})
        )
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control',         'placeholder': field.label })
            
    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email","assigned_to", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password = forms.CharField(max_length=128, required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))

class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomUser
        fields = ['username','email','first_name','last_name','assigned_to','is_active','is_staff','is_superuser']

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
        fields = ['username','password1','password2','email','first_name','last_name', 'assigned_to', 'is_active','is_staff','is_superuser']

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

        if 'dob' in self.fields:
            self.fields['dob'].label = 'Birth Date'

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Tourist
        fields = '__all__'
        widgets = {
            'dob': forms.DateInput({'type': 'date'}),
        }

class SpotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpotForm, self).__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Spot
        fields = '__all__'
