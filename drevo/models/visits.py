from django.db import models
from users.models import User


class Visits(models.Model):
    """
    Просмотры
    """
    znanie = models.ForeignKey(
        'Znanie',
        models.CASCADE
    )
    user = models.ForeignKey(
        User,
        models.CASCADE
    )

    objects = models.Manager()
