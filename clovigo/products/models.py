from django.db import models
from core.globalchoices import (PRODUCTS_CHOICES,
                                COLOR_CHOICES,
                                RATING_CHOICES)
from core.models import  ColorModel
from accounts.models import (SellerModel,
                             CustomerModel)
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug from name
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")
        super().save(*args, **kwargs)

class ProductModel(models.Model):
    seller = models.ForeignKey(SellerModel, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    description = models.TextField()
    product_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, null=True, blank=True)
    color_available = models.ForeignKey(ColorModel, on_delete=models.SET_NULL, null=True, blank=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES)
    trend_order = models.IntegerField()

    # Pricing
    actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Enter a discount between 1 and 100"
    )
    stocks = models.PositiveIntegerField()

    # Packaging & Dates
    pack_size = models.CharField(max_length=50, help_text="e.g., '1 Kg', '500 g', '2L'" ,null=True)
    mfg_date = models.DateField(verbose_name="Manufacturing Date", null=True)
    expiry_date = models.DateField(verbose_name="Expiry Date", null= True)

    # Policy & Logistics
    is_return_policy = models.BooleanField(default=False)
    return_before = models.CharField(max_length=255)
    delivered_within = models.CharField(max_length=255)

    # Media
    image = models.ImageField(upload_to="images/")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    @property
    def calculated_discount_price(self):
        return round(self.actual_price * (1 - (self.discount_percentage / 100)), 2)

    def clean(self):
        from django.core.exceptions import ValidationError
        if self.expiry_date <= self.mfg_date:
            raise ValidationError("Expiry date must be after the manufacturing date.")


class ReviewModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.CharField(max_length=10, choices=RATING_CHOICES)
    customer = models.ForeignKey(CustomerModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.customer} - {self.product} ({self.rating})"

