# Definicje formularzy m.in. na podstawie modeli
from django.forms import ModelForm
from django import forms
from .models import Movie

class MovieForm(ModelForm):

    class Meta:
        model = Movie
        fields = "__all__"
        #exclude = ("pola do wyłączenia",)

# Formularz bez modelu na bazie klasy forms.Form
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=50, initial="Imię", min_length=2)
    last_name = forms.CharField()
    email = forms.EmailField(help_text="Podaj adres email")
    age = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean_first_name(self):
        s = self.cleaned_data["first_name"]
        if len(s)<2:
            raise forms.ValidationError("Za krótki tekst")
        return self.cleaned_data["first_name"]

    def clean_age(self):
        age = self.cleaned_data["age"]
        if age<0 or age>110:
            raise forms.ValidationError("Niepoprawna wartość w polu wiek")
        return age

    def clean_password2(self):
        s1 = self.cleaned_data["password1"]
        s2 = self.cleaned_data["password2"]
        if s1!=s2:
            raise forms.ValidationError("Problem z hasłem")
        return s1

    def clean(self):
        form_data = self.cleaned_data
        return form_data
