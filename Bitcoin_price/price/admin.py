from django.contrib import admin
from .models import bitcoin_price, bitcoin
# Register your models here.


from .models import bitcoin_price
# ...
@admin.register(bitcoin_price)
class bitcoin_priceAdmin(admin.ModelAdmin):
    list_display = ['Symbol', 'price', 'time']

@admin.register(bitcoin)
class bitcoin(admin.ModelAdmin):
    list_display = ['Symbol', 'price', 'time']
    
# admin.site.register(bitcoin_price)
