from django.contrib import admin
from .models import Table

class TableAdmin(admin.ModelAdmin):
    list_display = ('title', 'size', 'price', 'sellprice', 'anyprice', 'datebuy', 'datesell', 'value', 'notes')
    list_filter = ('title', 'price', 'sellprice', 'datebuy', 'datesell', 'value')
    search_fields = ('title', 'datebuy', 'datesell')




admin.site.register(Table, TableAdmin)