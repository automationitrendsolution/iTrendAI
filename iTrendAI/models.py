from django.db import models


class ResearchReport(models.Model):
    product_name = models.CharField(max_length=255)
    category     = models.CharField(max_length=255)
    file_name    = models.CharField(max_length=255, default='—')
    ai_output    = models.TextField()
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product_name} ({self.created_at.strftime('%d %b %Y')})"
