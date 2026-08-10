from django.db import models

# Create your models here.

class QuoteRequest(models.Model):
    SERVICE_CHOICES = [
        ('House Removal', 'House Removal'),
        ('Interstate Move', 'Interstate Move'),
        ('Office Relocation', 'Office Relocation'),
        ('Small Pick & Drop', 'Small Pick & Drop'),
        ('Furniture Assembly', 'Furniture Assembly'),
        ('Rubbish Removal', 'Rubbish Removal'),
        ('Second Hand Appliances', 'Second-Hand Appliances'),
    ]

    MOVE_SIZE_CHOICES = [
        ('Single Item / Few Items', 'Single Item / Few Items'),
        ('1 Bedroom Apartment', '1 Bedroom Apartment'),
        ('2 Bedroom Apartment / House', '2 Bedroom Apartment / House'),
        ('3+ Bedroom House', '3+ Bedroom House'),
        ('Office / Commercial', 'Office / Commercial'),
    ]

    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    pickup_location = models.CharField(max_length=200)
    dropoff_location = models.CharField(max_length=200)
    move_size = models.CharField(max_length=50, choices=MOVE_SIZE_CHOICES)
    move_date = models.DateField(null=True, blank=True)
    move_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.service_type} ({self.created_at.strftime('%Y-%m-%d')})"

    class Meta:
        ordering = ['-created_at']