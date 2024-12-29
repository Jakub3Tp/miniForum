from django.contrib import admin
from .models import Console
from .models import Comment
from .models import Rating
from .models import Profile

@admin.register(Console)
class ConsoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'nazwa', 'producent', 'data_premiery', 'autor', 'data_utworzenia', 'data_aktualizacji')
    search_fields = ('nazwa', 'producent')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'konsola', 'autor', 'tresc', 'data_utworzenia')
    search_fields = ('konsola', 'autor')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'konsola', 'autor', 'ocena', 'data_utworzenia')
    search_fields = ('konsola', 'autor')
    list_filter = ('ocena', 'konsola')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']