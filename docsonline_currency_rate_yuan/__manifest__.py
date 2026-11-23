{
    'name': 'Docs Online - Tasa de cambio del yuan (CNY)',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'license': 'LGPL-3',
    'author': 'Blanco Martín y Asociados SpA',
    'website': 'https://www.bmya.cl',
    'summary': 'Agrega el yuan (CNY) al proveedor de tasas mindicador cuando apunta a Docs Online.',
    'description': """
El proveedor de tasas de cambio «mindicador» (currency_rate_live) consulta una lista fija de
monedas: USD, EUR, UF y UTM. Activar el yuan (CNY) no basta para que Odoo pida su tasa.

Con este módulo, si el yuan está activo y el parámetro de sistema mindicador_api_url apunta al
servicio de tasas de cambio de Docs Online (documentosonline.cl/api/mindicador/...), Odoo
también pide {mindicador_api_url}/yuan/{fecha}, igual que las demás monedas. Docs Online lo
obtiene del Banco Central de Chile (pesos por yuan).

Si la URL apunta a mindicador.cl, que no publica el yuan, el módulo no hace nada. Un error al
obtener el yuan queda en el log y no impide actualizar las otras monedas.
""",
    'depends': [
        'currency_rate_live',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
