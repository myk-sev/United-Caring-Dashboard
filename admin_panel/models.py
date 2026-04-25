from django.db import models

# Create your models here.
class AdminSettings(models.Model):
    """
    Single-row table that holds the admin panel password.
    To be replaced with hashed password by collaborator when
    user authentication is added during testing phase.
    """
    admin_password = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Admin Settings"

    def __str__(self):
        return "Admin Settings"