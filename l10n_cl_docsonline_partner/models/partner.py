# -*- coding: utf-8 -*-
import json
import logging
import requests
import urllib
import time
from odoo import _, api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)

REGIONES = {
    "I REGION DE TARAPACA": "state_cl_01",
    "II REGION DE ANTOFAGASTA": "state_cl_02",
    "III REGION DE ATACAMA": "state_cl_03",
    "IV REGION COQUIMBO": "state_cl_04",
    "V REGION VALPARAISO": "state_cl_05",
    "VI REGION DEL LIBERTADOR GENERAL BERNARDO O'HIGGINS": "state_cl_06",
    "VII REGION DEL MAULE": "state_cl_07",
    "VIII REGION DEL BIO BIO": "state_cl_08",
    "IX REGION DE LA ARAUCANIA": "state_cl_09",
    "X REGION LOS LAGOS": "state_cl_10",
    "XII REGION DE MAGALLANES Y LA ANTARTICA CHILENA": "state_cl_12",
    "XIII REGION METROPOLITANA": "state_cl_13",
    "XIV REGION DE LOS RIOS": "state_cl_14",
    "XV REGION ARICA Y PARINACOTA": "state_cl_15",
    "XVI REGION DE ÑUBLE": "state_cl_16",
}

COMUNAS = {
    "AISEN": "city_cl_11201",
    "AYSEN": "city_cl_11201",
    "AYSÉN": "city_cl_11201",
    "ALGARROBO": "city_cl_05602",
    "ALHUE": "city_cl_13502",
    "ALTO BIOBIO": "city_cl_08314",
    "ALTO DEL CARMEN": "city_cl_03302",
    "ALTO HOSPICIO": "city_cl_01107",
    "ANCUD": "city_cl_10202",
    "ANDACOLLO": "city_cl_04103",
    "ANGOL": "city_cl_09201",
    "ANTARTICA": "city_cl_12202",
    "ANTOFAGASTA": "city_cl_02101",
    "ANTUCO": "city_cl_08302",
    "ARAUCO": "city_cl_08202",
    "ARICA": "city_cl_15101",
    "BUIN": "city_cl_13402",
    "BULNES": "city_cl_08402",
    "CABILDO": "city_cl_05402",
    "CABO DE HORNOS": "city_cl_12201",
    "CABRERO": "city_cl_08303",
    "CALAMA": "city_cl_02201",
    "CALBUCO": "city_cl_10102",
    "CALDERA": "city_cl_03102",
    "CALERA": "city_cl_05502",
    "CALERA DE TANGO": "city_cl_13403",
    "CALLE LARGA": "city_cl_05302",
    "CAMARONES": "city_cl_15102",
    "CAMINA": "city_cl_01402",
    "CANELA": "city_cl_04202",
    "CANETE": "city_cl_08203",
    "CARAHUE": "city_cl_09102",
    "CARTAGENA": "city_cl_05603",
    "CASABLANCA": "city_cl_05102",
    "CASTRO": "city_cl_10201",
    "CATEMU": "city_cl_05702",
    "CAUQUENES": "city_cl_07201",
    "CERRILLOS": "city_cl_13102",
    "CERRO NAVIA": "city_cl_13103",
    "CHAITEN": "city_cl_10401",
    "CHANARAL": "city_cl_03201",
    "CHANCO": "city_cl_07202",
    "CHEPICA": "city_cl_06302",
    "CHIGUAYANTE": "city_cl_08103",
    "CHILE CHICO": "city_cl_11401",
    "CHILLAN": "city_cl_08401",
    "CHILLAN VIEJO": "city_cl_08406",
    "CHIMBARONGO": "city_cl_06303",
    "CHOLCHOL": "city_cl_09121",
    "CHONCHI": "city_cl_10203",
    "CISNES": "city_cl_11202",
    "COBQUECURA": "city_cl_08403",
    "COCHAMO": "city_cl_10103",
    "COCHRANE": "city_cl_11301",
    "CODEGUA": "city_cl_06102",
    "COELEMU": "city_cl_08404",
    "COYHAIQUE": "city_cl_11101",
    "COIHAIQUE": "city_cl_11101",
    "COIHUECO": "city_cl_08405",
    "COINCO": "city_cl_06103",
    "COLBUN": "city_cl_07402",
    "COLCHANE": "city_cl_01403",
    "COLINA": "city_cl_13301",
    "COLLIPULLI": "city_cl_09202",
    "COLTAUCO": "city_cl_06104",
    "COMBARBALA": "city_cl_04302",
    "CONCEPCION": "city_cl_08101",
    "CONCHALI": "city_cl_13104",
    "CONCON": "city_cl_05103",
    "CONSTITUCION": "city_cl_07102",
    "CONTULMO": "city_cl_08204",
    "COPIAPO": "city_cl_03101",
    "COQUIMBO": "city_cl_04102",
    "CORONEL": "city_cl_08102",
    "CORRAL": "city_cl_14102",
    "CUNCO": "city_cl_09103",
    "CURACAUTIN": "city_cl_09203",
    "CURACAVI": "city_cl_13503",
    "CURACO DE VELEZ": "city_cl_10204",
    "CURANILAHUE": "city_cl_08205",
    "CURARREHUE": "city_cl_09104",
    "CUREPTO": "city_cl_07103",
    "CURICO": "city_cl_07301",
    "DALCAHUE": "city_cl_10205",
    "DIEGO DE ALMAGRO": "city_cl_03202",
    "DONIHUE": "city_cl_06105",
    "EL BOSQUE": "city_cl_13105",
    "EL CARMEN": "city_cl_08407",
    "EL MONTE": "city_cl_13602",
    "EL QUISCO": "city_cl_05604",
    "EL TABO": "city_cl_05605",
    "EMPEDRADO": "city_cl_07104",
    "ERCILLA": "city_cl_09204",
    "EST CENTRAL": "city_cl_13106",
    "FLORIDA": "city_cl_08104",
    "FREIRE": "city_cl_09105",
    "FREIRINA": "city_cl_03303",
    "FRESIA": "city_cl_10104",
    "FRUTILLAR": "city_cl_10105",
    "FUTALEUFU": "city_cl_10402",
    "FUTRONO": "city_cl_14202",
    "GALVARINO": "city_cl_09106",
    "GENERAL LAGOS": "city_cl_15202",
    "GORBEA": "city_cl_09107",
    "GRANEROS": "city_cl_06106",
    "GUAITECAS": "city_cl_11203",
    "HIJUELAS": "city_cl_05503",
    "HUALAIHUE": "city_cl_10403",
    "HUALANE": "city_cl_07302",
    "HUALPEN": "city_cl_08112",
    "HUALQUI": "city_cl_08105",
    "HUARA": "city_cl_01404",
    "HUASCO": "city_cl_03304",
    "HUECHURABA": "city_cl_13107",
    "ILLAPEL": "city_cl_04201",
    "INDEPENDENCIA": "city_cl_13108",
    "IQUIQUE": "city_cl_01101",
    "ISLA DE MAIPO": "city_cl_13603",
    "ISLA DE PASCUA": "city_cl_05201",
    "JUAN FERNANDEZ": "city_cl_05104",
    "LA CISTERNA": "city_cl_13109",
    "LA CRUZ": "city_cl_05504",
    "LA ESTRELLA": "city_cl_06202",
    "LA FLORIDA": "city_cl_13110",
    "LA GRANJA": "city_cl_13111",
    "LA HIGUERA": "city_cl_04104",
    "LA LIGUA": "city_cl_05401",
    "LA PINTANA": "city_cl_13112",
    "LA REINA": "city_cl_13113",
    "LA SERENA": "city_cl_04101",
    "LA UNION": "city_cl_14201",
    "LAGO RANCO": "city_cl_14203",
    "LAGO VERDE": "city_cl_11102",
    "LAGUNA BLANCA": "city_cl_12102",
    "LAJA": "city_cl_08304",
    "LAMPA": "city_cl_13302",
    "LANCO": "city_cl_14103",
    "LAS CABRAS": "city_cl_06107",
    "LAS CONDES": "city_cl_13114",
    "LAUTARO": "city_cl_09108",
    "LEBU": "city_cl_08201",
    "LICANTEN": "city_cl_07303",
    "LIMACHE": "city_cl_05505",
    "LINARES": "city_cl_07401",
    "LITUECHE": "city_cl_06203",
    "LLANQUIHUE": "city_cl_10107",
    "LLAY LLAY": "city_cl_05703",
    "LO BARNECHEA": "city_cl_13115",
    "LO ESPEJO": "city_cl_13116",
    "LO PRADO": "city_cl_13117",
    "LOLOL": "city_cl_06304",
    "LONCOCHE": "city_cl_09109",
    "LONGAVI": "city_cl_07403",
    "LONQUIMAY": "city_cl_09205",
    "LOS ALAMOS": "city_cl_08206",
    "LOS ANDES": "city_cl_05301",
    "LOS ANGELES": "city_cl_08301",
    "LOS LAGOS": "city_cl_14104",
    "LOS MUERMOS": "city_cl_10106",
    "LOS SAUCES": "city_cl_09206",
    "LOS VILOS": "city_cl_04203",
    "LOTA": "city_cl_08106",
    "LUMACO": "city_cl_09207",
    "MACHALI": "city_cl_06108",
    "MACUL": "city_cl_13118",
    "MAFIL": "city_cl_14105",
    "MAIPU": "city_cl_13119",
    "MALLOA": "city_cl_06109",
    "MARCHIHUE": "city_cl_06204",
    "MARIA ELENA": "city_cl_02302",
    "MARIA PINTO": "city_cl_13504",
    "MARIQUINA": "city_cl_14106",
    "MAULE": "city_cl_07105",
    "MAULLIN": "city_cl_10108",
    "MEJILLONES": "city_cl_02102",
    "MELIPEUCO": "city_cl_09110",
    "MELIPILLA": "city_cl_13501",
    "MOLINA": "city_cl_07304",
    "MONTE PATRIA": "city_cl_04303",
    "MOSTAZAL": "city_cl_06110",
    "MULCHEN": "city_cl_08305",
    "NACIMIENTO": "city_cl_08306",
    "NANCAGUA": "city_cl_06305",
    "NATALES": "city_cl_12401",
    "NAVIDAD": "city_cl_06205",
    "NEGRETE": "city_cl_08307",
    "NINHUE": "city_cl_08408",
    "NIQUEN": "city_cl_08409",
    "NOGALES": "city_cl_05506",
    "NUEVA IMPERIAL": "city_cl_09111",
    "NUNOA": "city_cl_13120",
    "OHIGGINS": "city_cl_11302",
    "OLIVAR": "city_cl_06111",
    "OLLAGUE": "city_cl_02202",
    "OLMUE": "city_cl_05507",
    "OSORNO": "city_cl_10301",
    "OVALLE": "city_cl_04301",
    "PADRE HURTADO": "city_cl_13604",
    "PADRE LAS CASAS": "city_cl_09112",
    "PAIHUANO": "city_cl_04105",
    "PAILLACO": "city_cl_14107",
    "PAINE": "city_cl_13404",
    "PALENA": "city_cl_10404",
    "PALMILLA": "city_cl_06306",
    "PANGUIPULLI": "city_cl_14108",
    "PANQUEHUE": "city_cl_05704",
    "PAPUDO": "city_cl_05403",
    "PAREDONES": "city_cl_06206",
    "PARRAL": "city_cl_07404",
    "PEDRO AGUIRRE CERDA": "city_cl_13121",
    "PELARCO": "city_cl_07106",
    "PELLUHUE": "city_cl_07203",
    "PEMUCO": "city_cl_08410",
    "PENAFLOR": "city_cl_13605",
    "PENALOLEN": "city_cl_13122",
    "PENCAHUE": "city_cl_07107",
    "PENCO": "city_cl_08107",
    "PERALILLO": "city_cl_06307",
    "PERQUENCO": "city_cl_09113",
    "PETORCA": "city_cl_05404",
    "PEUMO": "city_cl_06112",
    "PICA": "city_cl_01405",
    "PICHIDEGUA": "city_cl_06113",
    "PICHILEMU": "city_cl_06201",
    "PINTO": "city_cl_08411",
    "PIRQUE": "city_cl_13202",
    "PITRUFQUEN": "city_cl_09114",
    "PLACILLA": "city_cl_06308",
    "PORTEZUELO": "city_cl_08412",
    "PORVENIR": "city_cl_12301",
    "POZO ALMONTE": "city_cl_01401",
    "PRIMAVERA": "city_cl_12302",
    "PROVIDENCIA": "city_cl_13123",
    "PUCHUNCAVI": "city_cl_05105",
    "PUCON": "city_cl_09115",
    "PUDAHUEL": "city_cl_13124",
    "PUENTE ALTO": "city_cl_13201",
    "PUERTO MONTT": "city_cl_10101",
    "PUERTO OCTAY": "city_cl_10302",
    "PUERTO VARAS": "city_cl_10109",
    "PUMANQUE": "city_cl_06309",
    "PUNITAQUI": "city_cl_04304",
    "PUNTA ARENAS": "city_cl_12101",
    "PUQUELDON": "city_cl_10206",
    "PUREN": "city_cl_09208",
    "PURRANQUE": "city_cl_10303",
    "PUTAENDO": "city_cl_05705",
    "PUTRE": "city_cl_15201",
    "PUYEHUE": "city_cl_10304",
    "QUEILEN": "city_cl_10207",
    "QUELLON": "city_cl_10208",
    "QUEMCHI": "city_cl_10209",
    "QUILACO": "city_cl_08308",
    "QUILICURA": "city_cl_13125",
    "QUILLECO": "city_cl_08309",
    "QUILLON": "city_cl_08413",
    "QUILLOTA": "city_cl_05501",
    "QUILPUE": "city_cl_05106",
    "QUINCHAO": "city_cl_10210",
    "QUINTA DE TILCOCO": "city_cl_06114",
    "QUINTA NORMAL": "city_cl_13126",
    "QUINTERO": "city_cl_05107",
    "QUIRIHUE": "city_cl_08414",
    "RANCAGUA": "city_cl_06101",
    "RANQUIL": "city_cl_08415",
    "RAUCO": "city_cl_07305",
    "RECOLETA": "city_cl_13127",
    "RENAICO": "city_cl_09209",
    "RENCA": "city_cl_13128",
    "RENGO": "city_cl_06115",
    "REQUINOA": "city_cl_06116",
    "RETIRO": "city_cl_07405",
    "RINCONADA": "city_cl_05303",
    "RIO BUENO": "city_cl_14204",
    "RIO CLARO": "city_cl_07108",
    "RIO HURTADO": "city_cl_04305",
    "RIO IBANEZ": "city_cl_11402",
    "RIO NEGRO": "city_cl_10305",
    "RIO VERDE": "city_cl_12103",
    "ROMERAL": "city_cl_07306",
    "SAAVEDRA": "city_cl_09116",
    "SAGRADA FAMILIA": "city_cl_07307",
    "SALAMANCA": "city_cl_04204",
    "SAN ANTONIO": "city_cl_05601",
    "SAN BERNARDO": "city_cl_13401",
    "SAN CARLOS": "city_cl_08416",
    "SAN CLEMENTE": "city_cl_07109",
    "SAN ESTEBAN": "city_cl_05304",
    "SAN FABIAN": "city_cl_08417",
    "SAN FELIPE": "city_cl_05701",
    "SAN FERNANDO": "city_cl_06301",
    "SAN GREGORIO": "city_cl_12104",
    "SAN IGNACIO": "city_cl_08418",
    "SAN JAVIER": "city_cl_07406",
    "SAN JOAQUIN": "city_cl_13129",
    "SAN JOSE DE MAIPO": "city_cl_13203",
    "SAN JUAN DE LA COSTA": "city_cl_10306",
    "SAN MIGUEL": "city_cl_13130",
    "SAN NICOLAS": "city_cl_08419",
    "SAN PABLO": "city_cl_10307",
    "SAN PEDRO": "city_cl_13505",
    "SAN PEDRO DE ATACAMA": "city_cl_02203",
    "SAN PEDRO DE LA PAZ": "city_cl_08108",
    "SAN RAFAEL": "city_cl_07110",
    "SAN RAMON": "city_cl_13131",
    "SAN ROSENDO": "city_cl_08310",
    "SAN VICENTE": "city_cl_06117",
    "SANTA BARBARA": "city_cl_08311",
    "SANTA CRUZ": "city_cl_06310",
    "SANTA JUANA": "city_cl_08109",
    "SANTA MARIA": "city_cl_05706",
    "SANTIAGO": "city_cl_13101",
    "SANTO DOMINGO": "city_cl_05606",
    "SIERRA GORDA": "city_cl_02103",
    "TALAGANTE": "city_cl_13601",
    "TALCA": "city_cl_07101",
    "TALCAHUANO": "city_cl_08110",
    "TALTAL": "city_cl_02104",
    "TEMUCO": "city_cl_09101",
    "TENO": "city_cl_07308",
    "TEODORO SCHMIDT": "city_cl_09117",
    "TIERRA AMARILLA": "city_cl_03103",
    "TIL TIL": "city_cl_13303",
    "TIMAUKEL": "city_cl_12303",
    "TIRUA": "city_cl_08207",
    "TOCOPILLA": "city_cl_02301",
    "TOLTEN": "city_cl_09118",
    "TOME": "city_cl_08111",
    "TORRES DEL PAINE": "city_cl_12402",
    "TORTEL": "city_cl_11303",
    "TRAIGUEN": "city_cl_09210",
    "TREHUACO": "city_cl_08420",
    "TUCAPEL": "city_cl_08312",
    "VALDIVIA": "city_cl_14101",
    "VALLENAR": "city_cl_03301",
    "VALPARAISO": "city_cl_05101",
    "VICHUQUEN": "city_cl_07309",
    "VICTORIA": "city_cl_09211",
    "VICUNA": "city_cl_04106",
    "VILCUN": "city_cl_09119",
    "VILLA ALEGRE": "city_cl_07407",
    "VILLA ALEMANA": "city_cl_05108",
    "VILLARRICA": "city_cl_09120",
    "VINA DEL MAR": "city_cl_05109",
    "VITACURA": "city_cl_13132",
    "YERBAS BUENAS": "city_cl_07408",
    "YUMBEL": "city_cl_08313",
    "YUNGAY": "city_cl_08421",
    "ZAPALLAR": "city_cl_05405",
}


class ResPartner(models.Model):
    _inherit = 'res.partner'

    backup_name = fields.Char('Backup Name')

    def _fetch_docsonline_partner_data(self, endpoint, value, include_sucursales=False):
        """Fetch data from DocsOnline API for a given endpoint and value.
        Args:
            endpoint (str): API endpoint to call (e.g., 'partner/search', 'partner/details').
            value (str): Value to pass to the endpoint (e.g., RUT or search term).
            include_sucursales (bool): If True, add include_sucursales query parameter.
        Returns:
            dict: JSON data from the API response.
        Raises:
            UserError: If the API call fails or the response is invalid.
        """
        docsonline_data = self._get_docsonline_data()
        headers = {
            'Authorization': docsonline_data['token'],
            'accept': 'application/json',
        }
        try:
            encoded_value = urllib.parse.quote(value)
            url = f"{docsonline_data['url']}/{endpoint}/{encoded_value}"
            if include_sucursales:
                url += "?include_sucursales=True"
            start_time = time.time()
            _logger.debug(f"Requesting {url} with value: {value}")
            response = requests.get(
                url,
                headers=headers,
                timeout=90,
            )
            response.raise_for_status()
            end_time = time.time()
            _logger.debug(f"Response received in {end_time - start_time:.2f} seconds: {response.text[:200]}...")
        except requests.RequestException as e:
            _logger.error(f"DocsumentosOnline: Error API para {endpoint}/{value}: {str(e)}, Respuesta: {getattr(e.response, 'text', 'No response')}")
            if e.response:
                if e.response.status_code in [404, 500]:
                    try:
                        data = e.response.json()
                        error_msg = data.get('error', data.get('detail', str(e)))
                        return {'error': error_msg}
                    except json.JSONDecodeError:
                        return {'error': str(e)}
            raise UserError(_('DocumentosOnline: %s') % str(e))
        try:
            data = response.json()
            _logger.debug("DocumentosOnline: %s/%s: %s", endpoint, value, data)
            return data
        except json.JSONDecodeError:
            _logger.error("Invalid JSON response for %s/%s: %s", endpoint, value, response.text)
            raise UserError(_('DocsOnline: Invalid response format'))

    def _process_dol_data(self, partner_values):
        list_partner_data = []
        start_time = time.time()
        _logger.debug(f"Processing partner_values: {partner_values}")
        for key, list_data in partner_values.items():
            for data in list_data:
                partner_odoo_data = self._prepare_data_entry(data, is_branch=False, for_wizard=True)
                list_partner_data.append(partner_odoo_data)
        end_time = time.time()
        _logger.debug(f"Processed {len(list_partner_data)} entries in {end_time - start_time:.2f} seconds")
        return list_partner_data

    def _capital_preferences(self, value):
        """Capitalize text according to specific rules for partner data.
        Args:
            value (str): Text to capitalize.
        Returns:
            str: Capitalized text with specific replacements.
        """
        if not value:
            return ''
        abbreviation_replacement = {
            'Spa': 'SpA',
            'S.a.': 'S.A.',
            ' Y ': ' y ',
        }
        value = value.title()
        for k, v in abbreviation_replacement.items():
            if k in value:
                value = value.replace(k, v)
        return value

    def _get_partner_location_id(self, city):
        """Get the ID of a city from the database.
        Args:
            city (str): Name of the city to search for coming from webservice.
        Returns:
            int: ID of the city if found, False otherwise.
        """
        if not city:
            return False
        comuna_ref = COMUNAS.get(city)
        return self.env.ref(f'l10n_cl_counties.{comuna_ref}').id if comuna_ref else False

    def _get_partner_state_id(self, state):
        """Get the ID of a state/region from the database based on the region name.
        Args:
            state (str): Name of the state/region to search for.
        Returns:
            int: ID of the state if found, False otherwise.
        """
        if not state:
            return False
        state_ref = REGIONES.get(state)
        return self.env.ref(f'base.{state_ref}').id if state_ref else False

    def _prepare_data_entry(self, data, is_branch=False, for_wizard=False):
        address_data = data.get('contacto', {})
        city = address_data.get('comuna', False)

        if for_wizard:
            # Wizard-specific fields only
            base_data = {
                'name': self._capital_preferences(data.get('razon_social', False)),
                'vat': data.get('rut', ''),
                'street': self._capital_preferences(
                    f"{address_data.get('calle', '')} {address_data.get('numero', '')} "
                    f"{address_data.get('departamento', '')} {address_data.get('bloque', '')}"
                ).strip(),
                'city': self._capital_preferences(city),
                'l10n_cl_activity_description': self._capital_preferences(data.get('giro', '')),
            }
        else:
            # Full partner or branch data
            base_data = {
                'name': self._capital_preferences(data.get('razon_social', False)),
                'vat': data.get('rut', ''),
                'street': self._capital_preferences(
                    f"{address_data.get('calle', '')} {address_data.get('numero', '')}"
                ).strip(),
                'street2': self._capital_preferences(
                    f"{address_data.get('departamento', '')} {address_data.get('bloque', '')}"
                ).strip(),
                'city': self._capital_preferences(city),
                'city_id': self._get_partner_location_id(address_data.get('comuna', '')),
                'state_id': self._get_partner_state_id(address_data.get('region', None)),
                'country_id': self.env.ref('base.cl').id,
                'l10n_cl_activity_description': self._capital_preferences(data.get('giro', '')),
            }
            if not is_branch:
                base_data.update({
                    'l10n_latam_identification_type_id': self.env.ref('l10n_cl.it_RUT').id,
                    'l10n_cl_sii_taxpayer_type': '1',
                    'l10n_cl_dte_email': data.get('email_intercambio', ''),
                })

        return base_data

    def _prepare_single_partner_data(self, partner_values):
        return self._prepare_data_entry(partner_values, is_branch=False)

    def _get_docsonline_data(self):
        """Get configuration data for DocsOnline API.

        Returns:
            dict: Dictionary with API URL and token.
        """
        conf = self.env['ir.config_parameter'].sudo()
        return {
            'url': conf.get_param('docsonline.url'),
            'token': conf.get_param('docsonline.token'),
        }

    def _send_notification(self, msg_type, msg, sticky=False):
        self.env.user._bus_send('simple_notification', {
            'type': msg_type,
            'message': msg,
            'sticky': sticky,
        })

    def call_wizard(self):
        """Launch a wizard to select a partner from DocsOnline data.

        Returns:
            dict: Action dictionary to open the wizard.
        """
        self.ensure_one()
        partner_values = self._fetch_docsonline_partner_data('partner/search', self.name)
        if 'error' in partner_values:
            raise UserError(_('DocumentosOnline: %s') % partner_values['error'])
        wizard_obj = self.env['res.partner.docs.online']
        wizard_obj_data = self.env['res.partner.docs.online.data']
        wizard_obj.truncate()
        wizard_obj_data.truncate()
        wizard_id = wizard_obj.create({'partner_id': self.id})
        list_partner_data = self._process_dol_data(partner_values)

        sorted_list_partner_data = sorted(list_partner_data, key=lambda p: p.get('name', ''))

        for partner_odoo_data in sorted_list_partner_data:
            _logger.info("Creating wizard data: %s", partner_odoo_data)
            wizard_obj_data.create(partner_odoo_data)
        self._send_notification('success', _('Se encontraron coincidencias. Seleccione una de la lista'))
        self.env.cr.commit()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Select a partner from a list'),
            'res_model': 'res.partner.docs.online',
            'view_mode': 'form',
            'target': 'new',
            'res_id': wizard_id.id,
            'view_type': 'form',
            'view_id': self.env.ref('l10n_cl_docsonline_partner.tree_docsonline_partners_view').id,
            'active_id': wizard_id.id,
        }

    def _get_data_from_docsonline(self, rut_input=False):
        self.ensure_one()
        self.l10n_latam_identification_type_id = self.env.ref('l10n_cl.it_RUT')
        if not rut_input and not self.vat:
            _logger.info("No RUT or name provided for DocsOnline query")
            return
        rut = rut_input or self.vat.replace('.', '')
        partner_values = self._fetch_docsonline_partner_data('partner/details', rut)
        if 'error' in partner_values:
            raise UserError(_('DocumentosOnline: %s') % partner_values['error'])
        if not partner_values.get('razon_social'):
            raise UserError(_('Data not found for RUT %s. Try searching on www.documentosonline.cl') % rut)

        partner_odoo_data = self._prepare_single_partner_data(partner_values)
        config_params = self.env['ir.config_parameter'].sudo()

        update_vals = {
            'vat': partner_odoo_data.get('vat', rut),
            'l10n_latam_identification_type_id': partner_odoo_data['l10n_latam_identification_type_id'],
            'l10n_cl_sii_taxpayer_type': partner_odoo_data['l10n_cl_sii_taxpayer_type'],
        }
        if config_params.get_param('docsonline.replace_name', False):
            update_vals['name'] = partner_odoo_data['name']
        if config_params.get_param('docsonline.replace_street', False):
            update_vals.update({
                'street': partner_odoo_data['street'],
                'street2': partner_odoo_data['street2'],
                'city': partner_odoo_data['city'],
                'city_id': partner_odoo_data['city_id'],
            })
        if config_params.get_param('docsonline.replace_email', False) or not self.l10n_cl_dte_email:
            update_vals['l10n_cl_dte_email'] = partner_odoo_data['l10n_cl_dte_email']
        if config_params.get_param('docsonline.replace_activity', False) or not self.l10n_cl_activity_description:
            update_vals['l10n_cl_activity_description'] = partner_odoo_data['l10n_cl_activity_description']

        self.update(update_vals)

    def press_to_update(self):
        """Update partner data from DocsOnline when the update button is pressed."""
        if not self.vat and not self.name:
            raise UserError(_('RUT or Name required for DocsOnline update'))
        rut_input = (self.vat or self.name).replace('.', '')
        self._get_data_from_docsonline(rut_input)

    @api.model
    def multiple_update(self):
        """Update multiple partners from DocsOnline data."""
        for r in self:
            try:
                r.press_to_update()
                _logger.info("Updated partner %s", r.id)
            except Exception as e:
                _logger.warning("Failed to update partner %s: %s", r.id, str(e))
                continue

    def _prepare_branch_data(self, parent_id, branches):
        """Prepare data for branch (sucursal) records based on domicile data.

        Args:
            parent_id (res.partner): The main partner record to use as parent.
            branches (list): List of branch data dictionaries from API response (e.g., 'domicilios').

        Returns:
            list: List of dictionaries representing branch records.
        """
        branch_data = []
        for branch in branches:
            city = branch.get('comuna', False)
            branch_data.append({
                'parent_id': parent_id.id,
                'name': self._capital_preferences(
                    f"{parent_id.name} - SUC: {branch.get('calle', '')} {branch.get('numero', '')}"
                ),
                'street': self._capital_preferences(
                    f"{branch.get('calle', '')} {branch.get('numero', '')}"
                ).strip(),
                'street2': self._capital_preferences(
                    f"{branch.get('departamento', '')} {branch.get('bloque', '')}"
                ).strip(),
                'city': self._capital_preferences(city),
                'city_id': self._get_partner_location_id(city),
                'state_id': self._get_partner_state_id(branch.get('region', None)),
                'country_id': self.env.ref('base.cl').id,
                'type': 'other',
                'is_company': True,
            })
        return branch_data
