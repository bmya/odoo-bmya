| Descripción | Nombre Técnico | Última Versión |
|-------------|----------------|----------------|
| Reduce los espacios en blanco (padding) y márgenes debajo del encabezado de la factura a un mínimo, y reduce los tamaños de los tipos de letra un 80% para tener mayor espacio en la factura. | account_more_invoice_space | 17.0.1.0.0 |
| Este módulo permite seleccionar una moneda diferente una vez que se ha creado la factura en borrador, y al hacerlo recorre todas las lineas de la factura y actualiza la moneda y el monto utilizando la tasa previamente seleccionada. | account_move_change_currency | 17.0.1.0.0 |
| En Odoo stándard, si se cambia la posición fiscal una vez que las lineas están configuradas, los impuestos permanecen inmutables. Este módulo permite que al cambiar la posición fiscal en la factura (de venta o de compra) se actualicen los impuestos en las líneas | account_move_change_fiscal_position | 17.0.1.0.0 |
| Módulo que permite que en servidores el administrador del servidor se identifique como representante de cualquier usuario, con fines de servicio técnico. Cada ingreso queda identificado en la plataforma | auth_server_admin_passwd_passkey | No Disponible |
| Odoo hizo un cambio en el código para que la fecha de la tasa que se usa en facturas, sea la fecha de factura y no la fecha contable, lo que generó múltiples problemas. Este módulo soluciona eso dando precedencia a la fecha contable. | invoice_rate_accounting_date | 17.0.1.0.0 |
| Agrega un campo de selección basado en el campo oficial city_id a los clientes/proveedores para disponer de las comunas de Chile. Es compatible con l10n_cl y con l10n_cl_edi (facturación electrónica oficial) porque copia el valor de la comuna al campo city. | l10n_cl_counties | 17.0.3.2.0 |
| Este modulo hace un hack, colocando las comunas como si fuesen regiones, con el objeto de poder usar las reglas originales de Odoo para determinar los transportes disponibles. No se recommienda usarlo si no se usa delivery | l10n_cl_counties_as_region | 17.0.1.0.0 |
| Establece un tipo de documento por defecto basado en el tipo de contribuyente (consumidor final->boleta, 1ra o 2da categoria de ventas -> factura, extranjero -> factura de exportación. | l10n_cl_default_document_type | 17.0.1.0.0 |
| Permite obtener datos tributarios de los clientes conectandose a www.documentosonline.cl. Requiere obtener una API de este sitio. Hay opción de uso gratuito. | l10n_cl_docsonline_partner | 17.0.2.0.2 |
| Ciertos clientes que usan SAP requieren que el proveedor coloque en el XML de la factura un QBLI, que es un código en cada linea que identifica el ítem de la orden de compra de este cliente. | l10n_cl_edi_qbli | No Disponible |
| Además permite que la deuda en el asiento contable se cargue a la empresa principal a pesar que se facture a una sucursal. | l10n_cl_edi_special_fields | No Disponible |
| Agrega Campos adicionales en el modelo stock como chofer, etc. utilizando el modulo de flota. | l10n_cl_edi_stock_special_fields | 17.0.1.0.0 |
| Ciertos clientes que usan SAP validan CdgVendedor y CdgIntRecep en la factura para identificar al proveedor y exigen que dicho campo no obligatorio esté en la factura. Este modulo resuelve ese gap. | l10n_cl_partner_extra_xml_identification | No Disponible |
| Permite ordenar los tipos de documentos de latinoamérica para dar prioridad a un documento por defecto | l10n_latam_default_document | 17.0.1.0.0 |
| Agrega una posicion fiscal enlazada a los tipos de documentos. | l10n_latam_document_fiscal_position | 17.0.1.0.0 |
|  | picking_from_xls | No Disponible |
|  | pos_order_fiscal_position | No Disponible |
| Este modulo modifica el formato de las ordenes de compra para adaptarse a los formatos chilenos (recuadro margen superior derecho). | purchase_order_report | 17.0.1.1.0 |
| Este modulo modifica el formato de las ordenes de venta para adaptarse a los formatos chilenos (recuadro margen superior derecho). | sale_order_report | No Disponible |