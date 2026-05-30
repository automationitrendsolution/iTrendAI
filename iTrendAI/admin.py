from django.contrib import admin
from .models import ResearchReport


@admin.register(ResearchReport)
class ResearchReportAdmin(admin.ModelAdmin):
    list_display    = ('product_name', 'category', 'file_name', 'created_at')
    list_filter     = ('category', 'created_at')
    search_fields   = ('product_name', 'category', 'file_name')
    ordering        = ('-created_at',)
    readonly_fields = ('created_at',)
