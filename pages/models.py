from django.db import models
from datetime import datetime

class ItemGroup(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    group = models.ForeignKey(ItemGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = models.FloatField(default=0)

    class Meta:
        unique_together = ('group', 'name')

    def __str__(self):
        if self.group:
            return f"{self.name} ({self.group.name})"
        return self.name

class QuotationTemplate(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class QuotationTemplateItem(models.Model):
    template = models.ForeignKey(QuotationTemplate, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qty = models.FloatField(default=1)
    unit_price = models.FloatField(null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def total_price(self):
        price = self.unit_price if self.unit_price is not None else self.item.unit_price
        return self.qty * price

    def __str__(self):
        return f"{self.item.name}"


class Quotation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('rejected', 'Rejected'),
        ('working', 'Working'),
        ('completed', 'Completed'),
    )
    reference = models.CharField(max_length=20, null=True, blank=True)

    title = models.CharField(max_length=255)
    client_name = models.CharField(max_length=255)
    template = models.ForeignKey(QuotationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    discount = models.FloatField(default=0)

    def total_amount(self):
        return sum(group.subtotal() for group in self.groups.all())

    def payable_amount(self):
        return self.total_amount() - self.discount

    def __str__(self):
        return f"{self.client_name} - {self.title}"

    def save(self, *args, **kwargs):
        if not self.reference:
            current_year = datetime.now().year % 100   # 2025 → 25
            current_month = datetime.now().month

            prefix = f"{current_year:02d}{current_month:02d}"  # 2506

            # ওই বছরের সর্বশেষ নম্বর বের করা
            last_quote = Quotation.objects.filter(reference__startswith=prefix).order_by('-reference').first()

            if last_quote:
                last_number = int(last_quote.reference[4:])  # 250601 → 0001
                new_number = last_number + 1
            else:
                new_number = 1

            # Format: 25 + 0001 → 250001
            self.reference = f"{prefix}{new_number:03d}"

        super().save(*args, **kwargs)

class QuotationGroup(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='groups')
    name = models.CharField(max_length=255)

    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    def __str__(self):
        return self.name


class QuotationItem(models.Model):
    group = models.ForeignKey(QuotationGroup, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.FloatField(default=0)
    unit_price = models.FloatField(default=0)
    total_price = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        # If the item is not from the master list, ensure it has a description.
        if not self.item and not self.description:
            raise ValueError("QuotationItem must have either an item or a description.")

        # If a description is provided without a master item, it's a custom item.
        if self.description and not self.item:
            # Optionally, you could create a temporary Item here if you need to,
            # but the goal is to avoid populating the master Item list.
            pass

        self.total_price = self.qty * self.unit_price
        super().save(*args, **kwargs)

    def __str__(self):
        return self.description or self.item.name