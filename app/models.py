from django.db import models

# Create your models here.
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    photo = models.ImageField(
        upload_to = "contact_photo/",
        default = "icon.svg",
        blank = True,
        null = True
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
