from django.db import models
from django.contrib.auth.models import User

class SocialAccount(models.Model):
    user = models.ForeignKey(User)
    social = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    access_token_secret = models.CharField(max_length=255, null=True, blank=True)
    token_expire = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.user, self.social)  

    class Meta:
        verbose_name_plural = "Social Accounts"

class AppData(models.Model):
    nome = models.CharField(max_length=50)
    app_id = models.CharField(max_length=255, null=True, blank=True)
    app_secret = models.CharField(max_length=255, null=True, blank=True)
    account = models.ManyToManyField(SocialAccount, null=True, blank=True)

    def __unicode__(self):
        return self.nome  

    class Meta:
        verbose_name_plural = "Apps Data"
