from django.contrib import admin
from .models import Table, Meetings, PotentialSellPrice


class TableAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'title', 'size', 'price', 'currencybuy', 'sellprice', 'currencysellprice', 'anyprice', 'datebuy', 'datesell', 'value', 'notes', 'meet', 'possibleprice')
    list_filter = ('userID', 'title', 'price', 'sellprice', 'datebuy', 'datesell', 'value')
    search_fields = ('userID', 'title', 'datebuy', 'datesell')


class MeetingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'title', 'sellpricesum', 'datemeeting', 'notes')
    list_filter = ('userID', 'title', 'sellpricesum', 'datemeeting')
    search_fields = ('userID', 'title', 'sellpricesum', 'datemeeting')


class PotentialSellPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'userID', 'potentialprice')
    list_filter = ('userID', 'potentialprice')
    search_fields = ('userID', )


admin.site.register(Table, TableAdmin)
admin.site.register(Meetings, MeetingsAdmin)
admin.site.register(PotentialSellPrice, PotentialSellPriceAdmin)
