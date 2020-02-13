from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='', blank=True, null=True, max_length=600)
    imagen = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    orden = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)],
                                blank=True)
    mostrar_caja = models.BooleanField(default=False, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True, default='')

    def __str__(self):
        return str(self.pk) + ' - ' + self.nombre


class Proveedor(models.Model):
    nombre = models.CharField(max_length=100)
    orden = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)],
                                blank=True)
    color = models.CharField(max_length=50, null=True, blank=True, default='')
    descripcion = models.TextField(default='', blank=True, null=True, max_length=600)
    direccion = models.TextField(default='', blank=True, null=True, max_length=600)
    observaciones = models.TextField(default='', blank=True, null=True, max_length=600)
    telefono = models.CharField(default='', blank=True, null=True, max_length=100)
    email = models.EmailField(default='', blank=True, null=True, max_length=100)
    id_tributario = models.CharField(default='', blank=True, null=True, max_length=100)

    def __str__(self):
        return str(self.pk) + ' - ' + self.nombre


class Producto(models.Model):

    # CONTENIDO DE LA VARIABLE
    UNIDAD = 'Unidades'
    KILOGRAMOS = 'Kilogramos'
    GRAMOS = 'Gramos'
    LITROS = 'Litros'
    MILI_LITROS = 'Mili-Litros'
    # OPCIONES EN EL CHARFIELD
    OPCIONES_UND = [
        (UNIDAD, 'Unidad'),
        (KILOGRAMOS, 'Kilogramos'),
        (GRAMOS, 'Gramos'),
        (LITROS, 'Litros'),
        (MILI_LITROS, 'Mili-Litros'),
    ]

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(default='', blank=True, null=True, max_length=600)
    imagen = models.ImageField(null=True, upload_to='images/', blank=True, default='')
    orden = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)],
                                blank=True)
    color = models.CharField(null=True, max_length=50, blank=True, default='')
    cantidad_venta = models.IntegerField(null=True, default=0, blank=True)
    coste = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    precio = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    impuesto = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ultimo_movimiento = models.DateTimeField(auto_now=True, blank=True, null=True)

    """ el modelo deberia seleccionarse de un conjunto cerrado de opciones"""
    unidad_medida = models.CharField(choices=OPCIONES_UND,default=UNIDAD, blank=True, null=True,max_length=20)
    mostrar_caja = models.BooleanField(default=False, null=True, blank=True)
    codigo_barra = models.CharField(default='', blank=True, null=True, max_length=100)
    stock_minimo = models.IntegerField(default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    stock_bodega = models.IntegerField(default=0, blank=True, null=True)

    """ el modelo deberia seleccionarse de un conjunto cerrado de opciones
    0=consumo cocina, 1=venta, 2=ambos, 3=elaborado"""
    tipo_producto = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(3)],
                                        blank=True)

    """ el modelo deberia seleccionarse de un conjunto cerrado de opciones
    0 = 'NO inventariable';1 = 'Bodega';2 = 'Salon/Bodega';3 = 'Salon' """
    estado_inv = models.IntegerField(null=True, default=0, validators=[MinValueValidator(0), MaxValueValidator(3)],
                                     blank=True)
    multiplicador_hijos = models.IntegerField(null=True, default=0,
                                              validators=[MinValueValidator(0), MaxValueValidator(100)], blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos_cat')
    proveedor = models.ManyToManyField(Proveedor, related_name='productos_prv')

    def __str__(self):
        return str(self.pk) + ' - ' + self.nombre


class Factura(models.Model):
    # CONTENIDO DE LA VARIABLE
    SalonAbierta = 0
    SalonCerrada = 1
    DomicilioAbierta = 2
    DomicilioCerrada = 3
    # OPCIONES EN EL CHARFIELD
    OPCIONES_FACT = [
        (SalonAbierta, 'Salon pdte. Pago'),
        (SalonCerrada, 'Salon Pagada'),
        (DomicilioAbierta, 'Domicilio pdte. Pago'),
        (DomicilioCerrada, 'Domicilio Pagado'),
    ]

    fecha_creacion = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    ultimo_cambio = models.DateTimeField(auto_now=True)
    total = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    pagado = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    descuento = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    recargo = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)

    """ el modelo deberia seleccionarse de un conjunto cerrado de opciones
        0 = 'Salon_Abierta';1 = 'Salon_Cerrada';2 = 'Domicilio_Abierta';3 = 'Domicilio_Cerrada' """
    tipo_fact = models.IntegerField(choices=OPCIONES_FACT,default=SalonAbierta,null=True,
                                    validators=[MinValueValidator(0), MaxValueValidator(3)],blank=True)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.total) + ' - ' + str(self.fecha_creacion) + ' - ' + str(self.ultimo_cambio)
    # zona venta
    # mesero
    # cliente
    # mesa
    # metodo_pago
    # impuesto
    # impuesto incluido


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.DO_NOTHING, related_name='facturados')
    ultimo_cambio = models.DateTimeField(auto_now=True)
    cant_venta = models.IntegerField(default=1, blank=False, null=False, validators=[MinValueValidator(1)])
    desc_prod = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    recargo_prod = models.DecimalField(null=True, default=0, blank=True, max_digits=1000, decimal_places=2)
    precio_real = models.DecimalField(null=False, default=0, blank=False, max_digits=1000, decimal_places=2)
    precio_venta = models.DecimalField(null=False, default=0, blank=False, max_digits=1000, decimal_places=2)
    venta_total = models.DecimalField(null=False, default=0, blank=False, max_digits=1000, decimal_places=2)

    def __str__(self):
        return str(self.pk) + ' - ' + str(self.factura)

    class Meta:
        unique_together = (('factura', 'producto'),)
        index_together = (('factura', 'producto'),)
