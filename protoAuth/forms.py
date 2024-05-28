from django import forms
from .models import Profile

class MyProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number', 'birthday', 'gender', 'user_type']

class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['professional_field', 'education', 'current_job', 'experience', 'location', 'personal_qualities', 'certificates', 'resume']
