from django import forms
from .models import Student,Teacher,Course
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'duration', 'fee']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'fee': forms.NumberInput(attrs={'class': 'form-control'}),
        }
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'subjects']
        labels = {
            'subjects': 'Select Subjects'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'subjects': forms.CheckboxSelectMultiple(),  
        }



class StudentForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data["name"]

        if any(char.isdigit() for char in name):
            raise ValidationError("Name should not contain digits.")

        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")

        return name

    def clean_email(self):
        email = self.cleaned_data["email"]

        if not email.endswith('@gmail.com'):
            raise ValidationError("Email must end with @gmail.com.")

        bad_domains = ["tempmail.com", "trashmail.com"]

        if any(email.endswith(domain) for domain in bad_domains):
            raise ValidationError("Fake email detected.")

        return email

    def clean_age(self):
        age = self.cleaned_data["age"]

        # Probably what you meant:
        if age < 3 or age > 60:
            raise ValidationError("You are not eligible.")

        return age

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        age = cleaned_data.get("age")

        if age and name and age > 10 and name.lower() == "admin":
            raise ValidationError("A student older than 10 cannot be named 'admin'.")

        return cleaned_data

    class Meta:
        model = Student
        fields = ['name', 'email', 'age', 'phone_number', 'course', 'teachers']
        labels = {
            'course': 'Select Course',
            'teachers': 'Select Teachers'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-select'}),   # SINGLE select
            'teachers': forms.CheckboxSelectMultiple(),               # MULTIPLE checkboxes
        }


class StudentCSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a .csv file"
    )