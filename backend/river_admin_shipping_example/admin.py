from django.contrib import admin

import river_admin
from river_admin.site import RiverAdmin
from river_admin_shipping_example.models import Shipping


class ShippingRiverAdmin(RiverAdmin):
    name = "Shipping Flow"
    icon = "mdi-truck"
    list_displays = ['pk', 'product', 'customer', 'shipping_status']


river_admin.site.register(Shipping, "shipping_status", ShippingRiverAdmin)


class ShippingAdmin(admin.ModelAdmin):
    readonly_fields = ('shipping_status',)


admin.site.register(Shipping, ShippingAdmin)
