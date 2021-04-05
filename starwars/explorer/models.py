from django.db import models


class Collections(models.Model):
    """
    Holds meta data for each Star Wars collection.
    """
    filename = models.FilePathField()
    created = models.DateTimeField(auto_now_add=True)
