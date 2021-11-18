from django.db import models
from django.core.validators import \
    MinValueValidator, MaxValueValidator, MinLengthValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User #  import klasy z dostępem do użytkowników

from datetime import datetime
import uuid
import os
# Create your models here.

def custom_file_upload(instance, filename):
    #return f"{str(uuid.uuid4())}/{filename}"
    return os.path.join(str(uuid.uuid4(),filename))

def check_descr(value):
    if "dupa" in value:
        raise ValidationError("Ale brzydko piszesz!!!")
    else:
        return value

custom_error_msg = {
    "null" : "To pole ma wartość NULL",
    "blank" : "To pole nie ma wprowadzonej wartości",
    "required" : "To pole jest obowiązkowe",
}

class Actor(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    class Meta:
        verbose_name = "Aktor"
        verbose_name_plural = "Aktorzy"


############ relacja one-2-many ########
class Comment(models.Model):
    body = models.TextField()
    stars = models.IntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    create_ts = models.DateTimeField(auto_now_add=True, editable=False)
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stars} - {self.body[:30]}"

    class Meta:
        verbose_name = "komentarz"
        verbose_name_plural = "komentarze"

# Model przechowujący dane o filmie
class Movie(models.Model):

    MPAA = (
        ('-' , 'Brak'),
        ('G' , 'Dla wszystkich'),
        ('PG-13' , 'Za zgodą rodziców'),
        ('NC-17' , 'Powyżej 17 roku życia'),
    )
    title = models.CharField(max_length=255, verbose_name="Tytuł filmu",
                             error_messages=custom_error_msg,
                             validators=[MinLengthValidator(2, message="Tytuł za krótki")])
    description = models.TextField(default="", verbose_name="Opis", validators=[check_descr])
    released = models.DateField(verbose_name="Data premiery", null=True, blank=True)
    year = models.IntegerField(editable=False, null=True, blank=True)
    imdb = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True,
                               validators=[MinValueValidator(1), MaxValueValidator(10)])
    mpaa_rating = models.CharField(choices=MPAA, max_length=10,
                                   verbose_name="MPAA", default='G')
    trailer_video = models.URLField(null=True, blank=True, verbose_name="Trailer")
    poster = models.ImageField(upload_to=custom_file_upload,  #"%Y%m%d",
                               null=True, blank=True, verbose_name="Plakat")
    create_ts = models.DateTimeField(auto_now_add=True, editable=False)
    update_ts = models.DateTimeField(auto_now=True, editable=False)
    update_ts_manual = models.DateTimeField(null=True, editable=False)

    author = models.ForeignKey(User, null=True, editable=False, on_delete=models.SET_NULL)

    # relacja M2M z modelem Actor
    actors = models.ManyToManyField(Actor, null=True, verbose_name="Aktorzy")

    def save(self, *args, **kwargs):
        if self.released:
            self.year = self.released.year
        if self.pk: # oznacza że jest już rekord, a jeśli None - to znaczy że dodajemy instancje obiektu
            self.update_ts_manual = datetime.today()
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"

# odbiorniki i sygnały
from django.db.models import signals
from django.dispatch import receiver

@receiver(signals.pre_save, sender=Movie)
def title_upper(sender, instance, **kwargs):
    instance.title = instance.title.upper()

@receiver(signals.post_save, sender=Movie)
def after_movie_save(sender, instance, created, **kwargs):
    print(created)