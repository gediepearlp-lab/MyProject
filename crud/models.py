from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    image = models.ImageField(
        upload_to='categories/',
        blank=True,
        null=True
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Supplier(models.Model):

    name = models.CharField(max_length=150)

    image = models.ImageField(
        upload_to='suppliers/',
        blank=True,
        null=True
    )

    contact_person = models.CharField(max_length=100, blank=True)

    phone = models.CharField(max_length=20, blank=True)

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# =========================
# INVENTORY ITEM MODEL
# =========================
class InventoryItem(models.Model):

    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('g', 'Gram'),
        ('L', 'Liter'),
        ('mL', 'Milliliter'),
        ('pcs', 'Pieces'),
        ('packs', 'Packs'),
        ('bags', 'Bags'),
        ('boxes', 'Boxes'),
    ]

    STATUS_CHOICES = [
        ('in_stock', 'In Stock'),
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
    ]

    name = models.CharField(
        max_length=150
    )

    # IMAGE FIELD
    image = models.ImageField(
        upload_to='inventory/',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items'
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='items'
    )

    sku = models.CharField(
        max_length=50,
        unique=True,
        help_text="Stock Keeping Unit"
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default='pcs'
    )

    reorder_level = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10
    )

    cost_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='items_created'
    )

    # ITEM STATUS
    @property
    def status(self):

        if self.quantity <= 0:
            return 'out_of_stock'

        elif self.quantity <= self.reorder_level:
            return 'low_stock'

        return 'in_stock'

    # TOTAL VALUE
    @property
    def total_value(self):
        return self.quantity * self.cost_price

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        ordering = ['name']


# =========================
# STOCK TRANSACTION MODEL
# =========================
class StockTransaction(models.Model):

    TRANSACTION_TYPES = [
        ('restock', 'Restock'),
        ('usage', 'Usage'),
        ('adjustment', 'Adjustment'),
        ('waste', 'Waste'),
    ]

    item = models.ForeignKey(
        InventoryItem,
        on_delete=models.CASCADE,
        related_name='transactions'
    )

    transaction_type = models.CharField(
        max_length=20,
        choices=TRANSACTION_TYPES
    )

    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"

    class Meta:
        ordering = ['-created_at']