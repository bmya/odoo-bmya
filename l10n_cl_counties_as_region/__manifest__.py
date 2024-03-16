
{
    "name": "Chile Localization Regions, Cities and Counties",
    "description": """
    This module allows to include the county (comuna) as if it were a region. The object of this 
    is to contain all the comunas in a single table.
    One application for this is to allow multiple delivery methods and using a rule by comuna instead
    of adding additional entropy to the module.
    NOTE: DO NOT INSTALL if you don't need to use delivery methods rules based on comunas.
    """,
    "version": "17.0.1.0",
    "author": "Blanco Martín & Asociados",
    'license': "LGPL-3",
    "website": "http://blancomartin.cl",
    "category": "Localization/Geopolitical Distribution",
    "depends": [
        "base",
        "l10n_cl_counties",
    ],
    "data": [
        "data/res.country.state.csv",
        "data/res.city.csv",
    ],
    "active": False,
    "installable": True,
}
