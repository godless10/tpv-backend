from rest_framework import serializers
from .models import Categoria,Proveedor,Producto,Factura,DetalleFactura



class ProductoSerial(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id','nombre','descripcion','imagen','orden','color','cantidad_venta',
                  'coste','precio','impuesto','fecha_creacion','ultimo_movimiento',
                  'unidad_medida','mostrar_caja','codigo_barra','stock_minimo',
                  'stock_bodega','tipo_producto','estado_inv','multiplicador_hijos',
                  'categoria','proveedor']


class CategoriaSerial(serializers.ModelSerializer):
    productos_cat = ProductoSerial(many=True)
    class Meta:
        model = Categoria
        fields = ['id','nombre','descripcion','imagen','orden','mostrar_caja',
                  'color','productos_cat']


class ProveedorSerial(serializers.ModelSerializer):
    productos_prv = ProductoSerial(many=True)
    class Meta:
        model = Categoria
        fields = ['id','nombre','descripcion','orden','color','id_tributario',
                  'observaciones','direccion','telefono','email','productos_prv']


class DetalleFacturaSerial(serializers.ModelSerializer):
    #producto = ProductoSerial(many=False)
    class Meta:
        model = DetalleFactura
        fields = ['id','factura','producto','ultimo_cambio','cant_venta',
                  'desc_prod','recargo_prod','precio_real','precio_venta',
                  'venta_total']


class FacturaSerial(serializers.ModelSerializer):
    detalles = DetalleFacturaSerial(many=True)
    class Meta:
        model = Factura
        fields = ['id','fecha_creacion','ultimo_cambio','total','pagado',
                  'descuento','recargo','tipo_fact','detalles']












