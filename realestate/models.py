from django.db import models
from user.models import User

# Create your models here.
class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('sale', 'Sale'),
        ('rent', 'Rent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveBigIntegerField()
    discount_price= models.PositiveBigIntegerField(null=True, blank= True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    published = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry by {self.user.username} for {self.listing.title}"