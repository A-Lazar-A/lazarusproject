from django.contrib import admin
from .models import Table

class TableAdmin(admin.ModelAdmin):
    list_display = ('userID', 'title', 'size', 'price', 'sellprice', 'anyprice', 'datebuy', 'datesell', 'value', 'notes')
    list_filter = ('userID', 'title', 'price', 'sellprice', 'datebuy', 'datesell', 'value')
    search_fields = ('userID', 'title', 'datebuy', 'datesell')




admin.site.register(Table, TableAdmin)