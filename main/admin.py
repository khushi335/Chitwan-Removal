from django.contrib import admin
from .models import QuoteRequest

# Register your models here.

@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'phone', 'email', 'service_type', 'move_date', 'move_time', 'created_at')
    list_filter = ('service_type', 'move_size', 'created_at')
    search_fields = ('full_name', 'phone', 'email', 'pickup_location', 'dropoff_location')
    readonly_fields = ('created_at',)