from django.contrib import admin
from .models import ProblemReport

@admin.register(ProblemReport)
class ProblemReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')
