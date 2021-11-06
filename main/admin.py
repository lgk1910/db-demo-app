from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(DigitalVersion)
admin.site.register(HardCopy)
admin.site.register(Warehouse)
admin.site.register(StoreInfo)
admin.site.register(Author)
admin.site.register(PublicationInfo)
admin.site.register(Keyword)
admin.site.register(Genre)
admin.site.register(Card)
admin.site.register(TransactionInfo)
admin.site.register(Cart)
admin.site.register(CartItem)