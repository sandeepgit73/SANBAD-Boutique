from django.core.management.base import BaseCommand
from store.models import Product

SAMPLES = [
    ("Floral Anarkali Suit", "Women", "2499.00", "Ethnic wear", "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=700&q=80"),
    ("Elegant Occasion Saree", "Women", "3299.00", "Festive edit", "https://images.unsplash.com/photo-1583391733956-6c78276477e4?auto=format&fit=crop&w=700&q=80"),
    ("Classic Casual Shirt", "Men", "1199.00", "Everyday style", "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=700&q=80"),
    ("Smart Men's Jacket", "Men", "2799.00", "Modern classic", "https://images.unsplash.com/photo-1617137968427-85924c800a22?auto=format&fit=crop&w=700&q=80"),
    ("Kids Party Outfit", "Kids", "1499.00", "Party wear", "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?auto=format&fit=crop&w=700&q=80"),
    ("Kids Everyday Set", "Kids", "899.00", "Comfort edit", "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?auto=format&fit=crop&w=700&q=80"),
    ("Women's Modern Dress", "Women", "1899.00", "New arrival", "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?auto=format&fit=crop&w=700&q=80"),
    ("Men's Casual T-shirt", "Men", "799.00", "Daily essential", "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=700&q=80"),
]

class Command(BaseCommand):
    help = "Add the SANBAD sample catalogue if the product table is empty."
    def handle(self, *args, **options):
        if Product.objects.exists():
            self.stdout.write(self.style.WARNING("Products already exist; no sample products added."))
            return
        for name, category, price, tag, image in SAMPLES:
            Product.objects.create(name=name, category=category, price=price, tag=tag, image_url=image, stock=10, description=f"Sample {category.lower()} fashion item from SANBAD.")
        self.stdout.write(self.style.SUCCESS("Added 8 sample products."))
