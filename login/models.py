from django.db import models
from django.contrib.auth.models import User


class Property(models.Model):
    PROPERTY_TYPE_CHOICES = [
        ('apartment', 'Residential Apartment'),
        ('villa', 'Villa'),
        ('plot', 'Plot / Land'),
    ]
    
    BEDROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3+', '3+'),
    ]
    
    BATHROOM_CHOICES = [
        ('1', '1'),
        ('2', '2'),
        ('3+', '3+'),
    ]
    
    # Seller Information
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    seller_first_name = models.CharField(max_length=100)
    seller_last_name = models.CharField(max_length=100)
    seller_email = models.EmailField()
    seller_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Property Details
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPE_CHOICES)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    bedrooms = models.CharField(max_length=10, choices=BEDROOM_CHOICES)
    bathrooms = models.CharField(max_length=10, choices=BATHROOM_CHOICES)
    description = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.property_type.upper()} in {self.location} - ₹{self.price}"


class PropertyImage(models.Model):
    """Model to store multiple images for each property"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.property}"