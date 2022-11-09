# 08/09/2022
* Se agrega filtro para entorno multiempresa en de certificado y servidor dentro de la empresa.
* Se mejora filtro en lineas de factura de venta, el tipo de impuesto de venta ya no se muestra en facturas de compra

# 13/09/2022
* Se establece un codigo de producto para el xml en caso el producto no cuente con uno y asi evitar enviar "-" que actualmente "devuelve aceptado con observaciones"
* Se actualiza la funcion "_ agregar_informacion_empresa" para tomar los datos desde una funcion, esto sirve para el modulo de multisucursal

* Se agrega configuracion para poder visualizar los montos totales de exonerados y demas tanto en el formulario como en la impresion (se tiene que modificar el grupo de tipo de impuesto activando el check "Mostrar base" de los registros que se requieran)

# 14/09/2022
* Se mejora la visualizacion del tipo de cambio dolar en la factura

# 02/10/2022
* Se arregla bug con el codigo de producto que se envia en el xml
* Se arregla bug que se tenia en algunos casos con el redondeo de la detracciones que se envia en el xml

# 07/10/2022
* Se arregla bug al ocultar/mostrar el tipo de documento en factura cuando se ingresa desde ventas

# 14/10/2022
* Se modifica reporte de factura para enlazar mejor con el modulo de guias electronicas

# 17/10/2022
* Se soluciona bug al emitir notas de detraccion en soles (se vio despues de la actualizacion de pagos detracion en dolares)

# 17/10/2022
* Se agrega etiqueta Type en el envio de clave para que sea admitido por OSE.
* Se mejora la visualizacion del tipo de pago credito, ahora muestra el nombre del plazo de pago seleccionado.

# 18/10/2022
* Se soluciona bug en la impresion del pdf cuando la factura es en dolares (salio con la actualizacion para visualizar las diferentes opereciones)

# 21/10/2022
* Se mejora visualizacion de descuento cuanto tiene muchos decimales
* Se aumenta el ancho del campo "Número" y "Cliente" en la vista lista de Facturas