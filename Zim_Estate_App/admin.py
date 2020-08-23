from django.contrib import admin
from .models import Buyer, Seller, Property, Contact

# Register your models here.


class PropertyAdmin(admin.ModelAdmin):
    #fields = '__all__'
    list_display = ('suburb', 'popularity', 'is_valid', 'seller', 'vacant', 'price')
    list_filter = ['price', 'property_type']
    search_fields = ['city', 'suburb']


class SellerAdmin(admin.ModelAdmin):
    #fields = '__all__'
    list_display = ('name', 'surname', 'email', )
    list_filter = ['surname', 'email']
    search_fields = ['surname']



class BuyerAdmin(admin.ModelAdmin):
    #fields = '__all__'
    list_display = ('name', 'property', 'email', )
    list_filter = ['name', 'property']
    search_fields = ['property']


class ContactAdmin(admin.ModelAdmin):
    #fields = '__all__'
    list_display = ('name', 'subject',  )
    list_filter = [ 'subject']
    search_fields = ['name']


admin.site.register(Buyer, BuyerAdmin)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Property, PropertyAdmin)



