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
    first_name = forms.CharField(max_length=50, initial="Imię")
    last_name = forms.CharField()
    email = forms.EmailField(help_text="Podaj adres email")
    age = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

