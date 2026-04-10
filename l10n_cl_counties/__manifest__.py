{
    "name": "Chile Localization Regions, Cities and Counties",
    "version": "17.0.3.2.0",
    "summary": "Agrega un campo de selección basado en el campo oficial city_id a los clientes/proveedores para disponer de las comunas de Chile. Es compatible con l10n_cl y con l10n_cl_edi (facturación electrónica oficial) porque copia el valor de la comuna al campo city. Compatible con localizacion oficial para Chile",
    "author": "Blanco Martín & Asociados",
    'license': "LGPL-3",
    "website": "http://blancomartin.cl",
    "category": "Localization/Geopolitical Distribution",
    "depends": [
        "l10n_cl",
        "base_address_extended",
    ],
    "data": [
        "data/res.city.csv",
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
    ],
    "installable": True,
}
