from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
import copy
from .models import Producto, Proveedor, Categoria, Factura, DetalleFactura
from .serializers import ProductoSerial, CategoriaSerial, ProveedorSerial, DetalleFacturaSerial, FacturaSerial
from django.contrib.auth.models import User


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerial
    # authentication_classes = (TokenAuthentication,)
    # allow any so the frontend can register users that are not already in the database
    permission_classes = (AllowAny,)

    # permission_classes = (IsAuthenticated,)

    # function triggered with the post method for specific products in the specific url
    # .../productos/id/facturacion/
    @action(detail=True, methods=['POST'])
    def factura_salon(self, request, pk=None):
        if 'factura_id' in request.data:
            factura = Factura.objects.get(id=request.data['factura_id'])
            producto = Producto.objects.get(id=pk)
            try:
                det_factura = DetalleFactura.objects.get(factura=factura, producto=producto)

                # Aux variables Detalle Factura (unique Register)
                cant_old = int(copy.deepcopy(det_factura.cant_venta))
                desc_prod_old = float(copy.deepcopy(det_factura.desc_prod))
                recargo_prod_old = float(copy.deepcopy(det_factura.recargo_prod))
                venta_total_old = float(copy.deepcopy(det_factura.venta_total))

                # Aux variables Factura
                ftotal = float(copy.deepcopy(factura.total))
                fdescuento = float(copy.deepcopy(factura.descuento))
                frecargo = float(copy.deepcopy(factura.recargo))

                # Quantity changed
                if 'cant_venta_total' in request.data:
                    cant_venta = request.data['cant_venta_total']
                    det_factura.cant_venta = int(cant_venta)
                else:
                    det_factura.cant_venta += 1

                # Extra charges changed
                if 'prod_recar' in request.data:
                    if recargo_prod_old != request.data['prod_recar']:
                        det_factura.recargo_prod = request.data['prod_recar']
                        frecargo -= recargo_prod_old * cant_old
                        frecargo += float(det_factura.recargo_prod )* int(det_factura.cant_venta)
                # Product Discount changed
                if 'prod_desc' in request.data:
                    if det_factura.desc_prod != request.data['prod_desc']:
                        det_factura.desc_prod = request.data['prod_desc']
                        fdescuento -= desc_prod_old * cant_old
                        fdescuento += float(det_factura.desc_prod) * int(det_factura.cant_venta)

                # getting all Detalle_factura fields ready
                precio_real = float(producto.precio)
                precio_venta = float(precio_real) - float(det_factura.desc_prod) + float(det_factura.recargo_prod)
                venta_total = int(det_factura.cant_venta) * float(precio_venta)
                det_factura.precio_venta = float(precio_venta)
                det_factura.venta_total = float(venta_total)

                # getting all Factura fields ready
                factura.descuento = fdescuento
                factura.recargo = frecargo
                # print(ftotal, "is of type", type(ftotal))
                # print(ftotal)
                ftotal -= venta_total_old
                ftotal += det_factura.venta_total

                factura.total = ftotal

                det_factura.save()
                factura.save()

                factura_serial = FacturaSerial(factura, many=False)
                response = {'message': 'FACTURA MODIFYING OLD product record', 'result': factura_serial.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                factura = Factura.objects.get(id=request.data['factura_id'])
                producto = Producto.objects.get(id=pk)
                # Aux variables Factura
                ftotal = float(copy.deepcopy(factura.total))
                fdescuento = float(copy.deepcopy(factura.descuento))
                frecargo = float(copy.deepcopy(factura.recargo))

                cant_venta = 1
                desc_prod = 0.0
                recargo_prod = 0.0
                if 'cant_venta_total' in request.data:
                    # print(int(request.data['cant_venta_total']), "is of type",type(int(request.data['cant_venta_total'])))
                    if int(request.data['cant_venta_total']) > 0:
                        cant_venta = request.data['cant_venta_total']
                if 'prod_desc' in request.data:
                    if float(request.data['prod_desc']) > 0:
                        desc_prod = float(request.data['prod_desc'])
                if 'prod_recar' in request.data:
                    if float(request.data['prod_recar']) > 0:
                        recargo_prod = float(request.data['prod_recar'])

                precio_real = float(producto.precio)
                precio_venta = float(precio_real) - float(desc_prod) + float(recargo_prod)
                venta_total = int(cant_venta) * float(precio_venta)
                det_factura = DetalleFactura.objects.create(factura=factura,
                                                            producto=producto,
                                                            cant_venta=cant_venta,
                                                            precio_real=precio_real,
                                                            precio_venta=precio_venta,
                                                            recargo_prod=recargo_prod,
                                                            desc_prod=desc_prod,
                                                            venta_total=venta_total
                                                            )

                fdescuento += float(det_factura.desc_prod) * int(det_factura.cant_venta)
                frecargo += float(det_factura.recargo_prod) * int(det_factura.cant_venta)
                ftotal += float(det_factura.venta_total)

                # getting all Factura fields ready
                factura.descuento = fdescuento
                factura.recargo = frecargo
                factura.total = ftotal
                factura.save()

                factura_serial = FacturaSerial(factura, many=False)
                response = {'message': 'FACTURA ADDING NEW product record', 'result': factura_serial.data}
                return Response(response, status=status.HTTP_200_OK)


        else:
            factura = Factura.objects.create(tipo_fact=0)
            producto = Producto.objects.get(id=pk)
            cant_venta = 1
            desc_prod = 0.0
            recargo_prod = 0.0
            if 'cant_venta_total' in request.data:
                # print(int(request.data['cant_venta_total']), "is of type", type(int(request.data['cant_venta_total'])))
                if int(request.data['cant_venta_total']) > 0:
                    cant_venta = request.data['cant_venta_total']
            if 'prod_desc' in request.data:
                if float(request.data['prod_desc']) > 0:
                    desc_prod = float(request.data['prod_desc'])
            if 'prod_recar' in request.data:
                if float(request.data['prod_recar']) > 0:
                    recargo_prod = float(request.data['prod_recar'])
            precio_real = float(producto.precio)
            precio_venta = float(precio_real) - float(desc_prod) + float(recargo_prod)
            venta_total = int(cant_venta) * float(precio_venta)
            det_factura = DetalleFactura.objects.create(factura=factura,
                                                        producto=producto,
                                                        cant_venta=cant_venta,
                                                        precio_real=precio_real,
                                                        precio_venta=precio_venta,
                                                        recargo_prod=recargo_prod,
                                                        desc_prod=desc_prod,
                                                        venta_total=venta_total
                                                        )
            # Modify a factura with details of the new product being added
            factura.descuento += float(det_factura.desc_prod) * int(det_factura.cant_venta)
            factura.recargo += float(det_factura.recargo_prod) * int(det_factura.cant_venta)
            factura.total += det_factura.venta_total
            factura.save()

            factura_serial = FacturaSerial(factura, many=False)
            # facturaDet_serial = DetalleFacturaSerial(det_factura, many=False)
            response = {'message': 'FACTURA has been CREATED!', 'result': factura_serial.data}
            return Response(response, status=status.HTTP_200_OK)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerial
    # authentication_classes = (TokenAuthentication,)
    # allow any so the frontend can register users that are not already in the database
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)


class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerial
    # authentication_classes = (TokenAuthentication,)
    # allow any so the frontend can register users that are not already in the database
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)


class DetalleFacturaViewSet(viewsets.ModelViewSet):
    queryset = DetalleFactura.objects.all()
    serializer_class = DetalleFacturaSerial
    # authentication_classes = (TokenAuthentication,)
    # allow any so the frontend can register users that are not already in the database
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)


class FacturaViewSet(viewsets.ModelViewSet):
    queryset = Factura.objects.all()
    serializer_class = FacturaSerial
    # authentication_classes = (TokenAuthentication,)
    # allow any so the frontend can register users that are not already in the database
    permission_classes = (AllowAny,)
    # permission_classes = (IsAuthenticated,)


def test(request):
    return HttpResponse('<h1>TEST</h1>')
