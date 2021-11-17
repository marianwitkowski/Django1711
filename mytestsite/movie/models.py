from django.db import models
import uuid
import os
# Create your models here.

def custom_file_upload(instance, filename):
    #return f"{str(uuid.uuid4())}/{filename}"
    return os.path.join(str(uuid.uuid4(),filename))


# Model przechowujący dane o filmie
class Movie(models.Model):

    MPAA = (
        ('-' , 'Brak'),
        ('G' , 'Dla wszystkich'),
        ('PG-13' , 'Za zgodą rodziców'),
        ('NC-17' , 'Powyżej 17 roku życia'),
    )
    title = models.CharField(max_length=255, verbose_name="Tytuł filmu")
    description = models.TextField(default="", verbose_name="Opis")
    released = models.DateField(verbose_name="Data premiery", null=True, blank=True)
    year = models.IntegerField(editable=False, null=True, blank=True)
    imdb = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    mpaa_rating = models.CharField(choices=MPAA, max_length=10,
                                   verbose_name="MPAA", default='G')
    trailer_video = models.URLField(null=True, blank=True, verbose_name="Trailer")
    poster = models.ImageField(upload_to=custom_file_upload,  #"%Y%m%d",
                               null=True, blank=True, verbose_name="Plakat")

    def save(self, *args, **kwargs):
        if self.released:
            self.year = self.released.year
        super(Movie, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmy"