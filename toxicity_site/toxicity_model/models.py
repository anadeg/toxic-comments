from django.db import models


class UserRequests(models.Model):
    username_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    request_text = models.TextField(max_length=10000)
    toxic = models.FloatField()
    severe_toxic = models.FloatField()
    obscene = models.FloatField()
    threat = models.FloatField()
    insult = models.FloatField()
    identity_hate = models.FloatField()
