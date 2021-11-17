from django.db import models

# Create your models here.

# Model przechowujący dane o filmie
class Movie(models.Model):
    title = models.CharField(max_length=255, verbose_name="Tytuł filmu")
    description = models.TextField(default="", verbose_name="Opis")
    released = models.DateField(verbose_name="Data premiery", null=True, blank=True)
    imdb = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"