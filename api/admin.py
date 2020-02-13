from django.contrib import admin
from .models import Producto,Categoria,Proveedor,Factura,DetalleFactura


admin.site.register(Producto)
admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(DetalleFactura)
admin.site.register(Factura)
