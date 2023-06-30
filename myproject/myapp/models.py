from django.db import models
from django.contrib.auth.models import User



class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # If user deletes his/her account, his/her fav movies also be deleted. We can also
    # use models.SET_NULL and items remain, not deleted.
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
