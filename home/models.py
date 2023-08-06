from django.db import models

# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=122)
    phone=models.CharField(max_length=13)
    email=models.CharField(max_length=133)
    content=models.TextField()
    date=models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "message from "+ self.name   