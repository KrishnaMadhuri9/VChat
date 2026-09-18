from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    class Meta:
        model=Register
        fields="__all__"

        widgets={
            'username':forms.TextInput(
                attrs={'class':'form-control'}
            ),

            'email':forms.EmailInput(
                attrs={'class':'form-control'}
            ),

            'dob':forms.DateInput(
                attrs={'type':'date',
                      'class':'form-control'}
            ),

            'gender':forms.Select(
                attrs={'class':'form-control'}
            ),

            'password':forms.PasswordInput(
                attrs={'class':'form-control'}
            )
        }

class LoginForm(forms.Form):
    username=forms.CharField(max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [
            "username",
            "email",
            "dob",
            "gender",
        ]

        widgets = {
            "dob": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control"
                }
            ),
        }