from django.db import models

# Create your models here.



class WhiteFlag(models.Model):
    record_number = models.AutoField(primary_key=True)
    men           = models.PositiveIntegerField(default=0)
    women         = models.PositiveIntegerField(default=0)
    children      = models.PositiveIntegerField(default=0)
    non_binary    = models.PositiveIntegerField(default=0)
    total         = models.PositiveIntegerField(default=0)
    submitted_at  = models.DateTimeField(auto_now_add=True)


    class Meta:
        app_label = 'whiteflag'
        ordering  = ['-submitted_at']

    def save(self, *args, **kwargs):
        self.total = self.men + self.women + self.children + self.non_binary
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Record #{self.record_number} — {self.submitted_at:%Y-%m-%d %H:%M}"
