from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [("Women", "Women"), ("Men", "Men"), ("Kids", "Kids")]
    name = models.CharField(max_length=160)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.CharField(max_length=80, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.category})"
