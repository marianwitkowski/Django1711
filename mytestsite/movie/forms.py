# Definicje formularzy m.in. na podstawie modeli
from django.forms import ModelForm
from django import forms
from .models import Movie

class MovieForm(ModelForm):

    class Meta:
        model = Movie
        fields = "__all__"
        #exclude = ("pola do wyłączenia",)



