from django.contrib import admin
from .models import Table, Meetings, PotentialSellPrice


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'title', 'size', 'price', 'currencybuy', 'sellprice', 'currencysell', 'anyprice', 'datebuy', 'datesell', 'value', 'notes', 'meet', 'possibleprice')
    list_filter = ('userID', 'title', 'price', 'sellprice', 'datebuy', 'datesell', 'value')
    search_fields = ('userID', 'title', 'datebuy', 'datesell')


class MeetingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'title', 'sellprice', 'datemeeting', 'notes')
    list_filter = ('userID', 'title', 'sellprice', 'datemeeting')
    search_fields = ('userID', 'title', 'sellprice', 'datemeeting')


class PotentialSellPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'potentialprice')
    list_filter = ('userID', 'potentialprice')
    search_fields = ('userID', )


admin.site.register(Table, TableAdmin)
admin.site.register(Meetings, MeetingsAdmin)
admin.site.register(PotentialSellPrice, PotentialSellPriceAdmin)
