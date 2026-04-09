| Descripción | Nombre Técnico | Última Versión |
|-------------|----------------|----------------|
| Este módulo permite seleccionar una moneda diferente una vez que se ha creado la factura en borrador, y al hacerlo recorre todas las lineas de la factura y actualiza la moneda y el monto utilizando la tasa previamente seleccionada. | account_move_change_currency | 18.0.1.0.0 |
| Módulo que permite que en servidores el administrador del servidor se identifique como representante de cualquier usuario, con fines de servicio técnico. Cada ingreso queda identificado en la plataforma | auth_server_admin_passwd_passkey | No Disponible |
| Agrega un campo de selección basado en el campo oficial city_id a los clientes/proveedores para disponer de las comunas de Chile. Es compatible con l10n_cl y con l10n_cl_edi (facturación electrónica oficial) porque copia el valor de la comuna al campo city. | l10n_cl_counties | 18.0.1.0.0 |
| Establece un tipo de documento por defecto basado en el tipo de contribuyente (consumidor final->boleta, 1ra o 2da categoria de ventas -> factura, extranjero -> factura de exportación. | l10n_cl_default_document_type | 18.0.1.0.0 |
| Permite obtener datos tributarios de los clientes conectandose a www.documentosonline.cl. Requiere obtener una API de este sitio. Hay opción de uso gratuito. | l10n_cl_docsonline_partner | 18.0.2.0.4 |
| Evita rechazos por parte del SII validando campos obligatorios | l10n_cl_edi_fix_validation | 18.0.1.0.0 |
| Ciertos clientes que usan SAP requieren que el proveedor coloque en el XML de la factura un QBLI, que es un código en cada linea que identifica el ítem de la orden de compra de este cliente. | l10n_cl_edi_qbli | 18.0.1.0.0 |
| Además permite que la deuda en el asiento contable se cargue a la empresa principal a pesar que se facture a una sucursal. | l10n_cl_edi_special_fields | 18.0.1.0.0 |
| Agrega Campos adicionales en el modelo stock como chofer, etc. utilizando el modulo de flota. | l10n_cl_edi_stock_special_fields | 18.0.1.0.0 |
| Ciertos clientes que usan SAP validan CdgVendedor y CdgIntRecep en la factura para identificar al proveedor y exigen que dicho campo no obligatorio esté en la factura. Este modulo resuelve ese gap. | l10n_cl_partner_extra_xml_identification | 18.0.1.0.0 |
| Módulo que permite la impresión de la factura cedible, como un documento separado a la factura. Incorpora en el PDF las leyendas para que la cedible sea firmada y la leyenda CEDIBLE | l10n_cl_report_invoice_cedible | 18.0.1.0.0 |
| Permite ordenar los tipos de documentos de latinoamérica para dar prioridad a un documento por defecto | l10n_latam_default_document | 18.0.1.0.0 |
|  | picking_from_xls | No Disponible |
| Este modulo modifica el formato de las ordenes de compra para adaptarse a los formatos chilenos (recuadro margen superior derecho). | purchase_order_report | 18.0.1.0.0 |
| Este modulo modifica el formato de las ordenes de venta para adaptarse a los formatos chilenos (recuadro margen superior derecho). | sale_order_report | No Disponible |