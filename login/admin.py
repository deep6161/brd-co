from django.contrib import admin
from login.models import Property, PropertyImage

# Register your models here.

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('property_type', 'location', 'price', 'bedrooms', 'bathrooms', 'seller_first_name', 'is_available', 'created_at')
    list_filter = ('property_type', 'is_available', 'bedrooms', 'bathrooms', 'created_at')
    search_fields = ('location', 'seller_first_name', 'seller_email')
    inlines = [PropertyImageInline]
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Seller Information', {
            'fields': ('seller_first_name', 'seller_last_name', 'seller_email', 'seller_phone')
        }),
        ('Property Details', {
            'fields': ('property_type', 'location', 'price', 'bedrooms', 'bathrooms', 'description', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)