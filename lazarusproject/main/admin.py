from django.contrib import admin
from .models import Table, Meetings


class TableAdmin(admin.ModelAdmin):
    list_display = ('userID', 'title', 'size', 'price', 'sellprice', 'anyprice', 'datebuy', 'datesell', 'value', 'notes')
    list_filter = ('userID', 'title', 'price', 'sellprice', 'datebuy', 'datesell', 'value')
    search_fields = ('userID', 'title', 'datebuy', 'datesell')


class MeetingsAdmin(admin.ModelAdmin):
    list_display = ('userID', 'iditem', 'title', 'sellprice', 'datemeeting', 'notes')
    list_filter = ('userID', 'title', 'sellprice', 'datemeeting')
    search_fields = ('userID', 'title', 'sellprice', 'datemeeting')


admin.site.register(Table, TableAdmin)
admin.site.register(Meetings, MeetingsAdmin)
