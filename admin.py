from django.contrib import admin
from django.db import models
from django import forms
from django_share.models import AppData, SocialAccount
from django_share.widgets import AccessTokenWidget

class SocialAccountForm(forms.ModelForm):
  class Meta:
    model = SocialAccount
    widgets = {
      'access_token': AccessTokenWidget(),
    }

class AppDataAdmin(admin.ModelAdmin):
    pass

class SocialAccountAdmin(admin.ModelAdmin):
    form = SocialAccountForm

admin.site.register(AppData, AppDataAdmin)
admin.site.register(SocialAccount, SocialAccountAdmin)
