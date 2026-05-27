from django.db import models


class ResearchProject(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
    ]

    niche = models.CharField(max_length=255)
    asin = models.CharField(max_length=20)
    uploaded_file = models.FileField(upload_to='helium_reports/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result = models.JSONField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.asin} – {self.niche}"


class ProductListing(models.Model):
    project = models.ForeignKey(ResearchProject, on_delete=models.CASCADE, related_name='listings')
    asin = models.CharField(max_length=20, blank=True)
    title = models.TextField(blank=True)
    brand = models.CharField(max_length=255, blank=True)
    seller_name = models.CharField(max_length=255, blank=True)
    seller_creation_date = models.DateField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    monthly_sales = models.IntegerField(null=True, blank=True)
    monthly_revenue = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    review_count = models.IntegerField(null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    image_count = models.IntegerField(null=True, blank=True)
    bsr = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.asin} – {self.title[:50]}"
