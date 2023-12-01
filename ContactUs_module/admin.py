from django.contrib import admin
from .models import ContactSubmission


# Register your models here.

class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'created_date', 'is_read_by_admin')
    list_filter = ('created_date', 'is_read_by_admin')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'message')


admin.site.register(ContactSubmission, ContactSubmissionAdmin)
