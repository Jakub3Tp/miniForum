from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.urls import reverse

class Console(models.Model):
    id = models.AutoField(primary_key=True)
    nazwa = models.CharField(max_length=255)
    producent = models.CharField(max_length=255)
    data_premiery = models.DateField()
    opis = models.TextField()
    zdjecie = models.ImageField(upload_to="media/")
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    data_utworzenia = models.DateTimeField(auto_now_add=True)
    data_aktualizacji = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nazwa

    def get_absolute_url(self):
        return reverse('console_detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    konsola = models.ForeignKey(Console, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField()
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Autor: {self.autor} \n Treść: {self.tresc}'

class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    konsola = models.ForeignKey(Console, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    ocena = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Ocena: {self.ocena}'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/',
                              blank=True)

    def __str__(self):
        return 'Profil użytkownika {}.'.format(self.user.username)
