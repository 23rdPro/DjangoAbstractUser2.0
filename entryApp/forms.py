from django import forms
from django.contrib.auth.models import User
from .models import Profile, Gender, MaritalStatus
from django.contrib.auth.forms import UserChangeForm, ReadOnlyPasswordHashField
from django.conf import settings


class DateInput(forms.DateInput):
    input_type = 'date'

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    gender = forms.ModelChoiceField(queryset=Gender.objects.all())
    marital_status = forms.ModelChoiceField(
        queryset=MaritalStatus.objects.all()
    )
    date_of_birth = forms.DateField()

    class Meta:
        model = Profile
        fields = (
            'username', 
            'gender', 
            'marital_status', 
            'first_name', 
            'last_name', 
            'date_of_birth',
            'number_of_children'
        )
        widgets = {
            "date_of_birth": DateInput()
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()
    gender = forms.ModelChoiceField(queryset=Gender.objects.all())
    marital_status = forms.ModelChoiceField(
        queryset=MaritalStatus.objects.all()
    )
    date_of_birth = forms.DateField()

    class Meta:
        model = Profile
        fields = (
            'username', 
            'gender', 
            'marital_status', 
            'first_name', 
            'last_name', 
            'date_of_birth',
            'number_of_children',
            'password',
        )
        widgets = {
            "date_of_birth": DateInput()
        }




