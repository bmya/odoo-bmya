import json
import logging
import time
import urllib

import requests

from odoo import fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

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
    "AISEN": "city_cl_276",
    "AYSEN": "city_cl_276",
    "AYSÉN": "city_cl_276",
    "ALGARROBO": "city_cl_72",
    "ALHUE": "city_cl_338",
    "ALTO BIOBIO": "city_cl_178",
    "ALTO DEL CARMEN": "city_cl_27",
    "ALTO HOSPICIO": "city_cl_11",
    "ANCUD": "city_cl_254",
    "ANDACOLLO": "city_cl_32",
    "ANGOL": "city_cl_221",
    "ANTARTICA": "city_cl_289",
    "ANTOFAGASTA": "city_cl_12",
    "ANTUCO": "city_cl_166",
    "ARAUCO": "city_cl_159",
    "ARICA": "city_cl_01",
    "BUIN": "city_cl_334",
    "BULNES": "city_cl_180",
    "CABILDO": "city_cl_60",
    "CABO DE HORNOS": "city_cl_288",
    "CABRERO": "city_cl_167",
    "CALAMA": "city_cl_16",
    "CALBUCO": "city_cl_245",
    "CALDERA": "city_cl_22",
    "CALERA": "city_cl_65",
    "CALERA DE TANGO": "city_cl_335",
    "CALLE LARGA": "city_cl_56",
    "CAMARONES": "city_cl_02",
    "CAMINA": "city_cl_06",
    "CANELA": "city_cl_37",
    "CANETE": "city_cl_160",
    "CARAHUE": "city_cl_201",
    "CARTAGENA": "city_cl_73",
    "CASABLANCA": "city_cl_46",
    "CASTRO": "city_cl_253",
    "CATEMU": "city_cl_78",
    "CAUQUENES": "city_cl_126",
    "CERRILLOS": "city_cl_296",
    "CERRO NAVIA": "city_cl_297",
    "CHAITEN": "city_cl_270",
    "CHANARAL": "city_cl_24",
    "CHANCO": "city_cl_127",
    "CHEPICA": "city_cl_107",
    "CHIGUAYANTE": "city_cl_148",
    "CHILE CHICO": "city_cl_282",
    "CHILLAN": "city_cl_179",
    "CHILLAN VIEJO": "city_cl_184",
    "CHIMBARONGO": "city_cl_108",
    "CHOLCHOL": "city_cl_220",
    "CHONCHI": "city_cl_255",
    "CISNES": "city_cl_277",
    "COBQUECURA": "city_cl_181",
    "COCHAMO": "city_cl_246",
    "COCHRANE": "city_cl_279",
    "CODEGUA": "city_cl_84",
    "COELEMU": "city_cl_182",
    "COYHAIQUE": "city_cl_274",
    "COIHAIQUE": "city_cl_274",
    "COIHUECO": "city_cl_183",
    "COINCO": "city_cl_85",
    "COLBUN": "city_cl_139",
    "COLCHANE": "city_cl_07",
    "COLINA": "city_cl_330",
    "COLLIPULLI": "city_cl_222",
    "COLTAUCO": "city_cl_86",
    "COMBARBALA": "city_cl_41",
    "CONCEPCION": "city_cl_146",
    "CONCHALI": "city_cl_298",
    "CONCON": "city_cl_47",
    "CONSTITUCION": "city_cl_117",
    "CONTULMO": "city_cl_161",
    "COPIAPO": "city_cl_21",
    "COQUIMBO": "city_cl_31",
    "CORONEL": "city_cl_147",
    "CORRAL": "city_cl_233",
    "CUNCO": "city_cl_202",
    "CURACAUTIN": "city_cl_223",
    "CURACAVI": "city_cl_339",
    "CURACO DE VELEZ": "city_cl_256",
    "CURANILAHUE": "city_cl_162",
    "CURARREHUE": "city_cl_203",
    "CUREPTO": "city_cl_118",
    "CURICO": "city_cl_129",
    "DALCAHUE": "city_cl_257",
    "DIEGO DE ALMAGRO": "city_cl_25",
    "DONIHUE": "city_cl_87",
    "EL BOSQUE": "city_cl_299",
    "EL CARMEN": "city_cl_185",
    "EL MONTE": "city_cl_343",
    "EL QUISCO": "city_cl_74",
    "EL TABO": "city_cl_75",
    "EMPEDRADO": "city_cl_119",
    "ERCILLA": "city_cl_224",
    "EST CENTRAL": "city_cl_300",
    "FLORIDA": "city_cl_149",
    "FREIRE": "city_cl_204",
    "FREIRINA": "city_cl_28",
    "FRESIA": "city_cl_247",
    "FRUTILLAR": "city_cl_248",
    "FUTALEUFU": "city_cl_271",
    "FUTRONO": "city_cl_234",
    "GALVARINO": "city_cl_205",
    "GENERAL LAGOS": "city_cl_04",
    "GORBEA": "city_cl_206",
    "GRANEROS": "city_cl_88",
    "GUAITECAS": "city_cl_278",
    "HIJUELAS": "city_cl_66",
    "HUALAIHUE": "city_cl_272",
    "HUALANE": "city_cl_130",
    "HUALPEN": "city_cl_157",
    "HUALQUI": "city_cl_150",
    "HUARA": "city_cl_08",
    "HUASCO": "city_cl_29",
    "HUECHURABA": "city_cl_301",
    "ILLAPEL": "city_cl_36",
    "INDEPENDENCIA": "city_cl_302",
    "IQUIQUE": "city_cl_05",
    "ISLA DE MAIPO": "city_cl_344",
    "ISLA DE PASCUA": "city_cl_54",
    "JUAN FERNANDEZ": "city_cl_48",
    "LA CISTERNA": "city_cl_303",
    "LA CRUZ": "city_cl_67",
    "LA ESTRELLA": "city_cl_101",
    "LA FLORIDA": "city_cl_304",
    "LA GRANJA": "city_cl_305",
    "LA HIGUERA": "city_cl_33",
    "LA LIGUA": "city_cl_59",
    "LA PINTANA": "city_cl_306",
    "LA REINA": "city_cl_307",
    "LA SERENA": "city_cl_30",
    "LA UNION": "city_cl_235",
    "LAGO RANCO": "city_cl_236",
    "LAGO VERDE": "city_cl_275",
    "LAGUNA BLANCA": "city_cl_285",
    "LAJA": "city_cl_168",
    "LAMPA": "city_cl_331",
    "LANCO": "city_cl_237",
    "LAS CABRAS": "city_cl_89",
    "LAS CONDES": "city_cl_308",
    "LAUTARO": "city_cl_207",
    "LEBU": "city_cl_158",
    "LICANTEN": "city_cl_131",
    "LIMACHE": "city_cl_68",
    "LINARES": "city_cl_138",
    "LITUECHE": "city_cl_102",
    "LLANQUIHUE": "city_cl_250",
    "LLAY LLAY": "city_cl_79",
    "LO BARNECHEA": "city_cl_309",
    "LO ESPEJO": "city_cl_310",
    "LO PRADO": "city_cl_311",
    "LOLOL": "city_cl_109",
    "LONCOCHE": "city_cl_208",
    "LONGAVI": "city_cl_140",
    "LONQUIMAY": "city_cl_225",
    "LOS ALAMOS": "city_cl_163",
    "LOS ANDES": "city_cl_55",
    "LOS ANGELES": "city_cl_165",
    "LOS LAGOS": "city_cl_238",
    "LOS MUERMOS": "city_cl_249",
    "LOS SAUCES": "city_cl_226",
    "LOS VILOS": "city_cl_38",
    "LOTA": "city_cl_151",
    "LUMACO": "city_cl_227",
    "MACHALI": "city_cl_90",
    "MACUL": "city_cl_312",
    "MAFIL": "city_cl_239",
    "MAIPU": "city_cl_313",
    "MALLOA": "city_cl_91",
    "MARCHIHUE": "city_cl_103",
    "MARIA ELENA": "city_cl_20",
    "MARIA PINTO": "city_cl_340",
    "MARIQUINA": "city_cl_240",
    "MAULE": "city_cl_120",
    "MAULLIN": "city_cl_251",
    "MEJILLONES": "city_cl_13",
    "MELIPEUCO": "city_cl_209",
    "MELIPILLA": "city_cl_337",
    "MOLINA": "city_cl_132",
    "MONTE PATRIA": "city_cl_42",
    "MOSTAZAL": "city_cl_92",
    "MULCHEN": "city_cl_169",
    "NACIMIENTO": "city_cl_170",
    "NANCAGUA": "city_cl_110",
    "NATALES": "city_cl_293",
    "NAVIDAD": "city_cl_104",
    "NEGRETE": "city_cl_171",
    "NINHUE": "city_cl_186",
    "NIQUEN": "city_cl_187",
    "NOGALES": "city_cl_69",
    "NUEVA IMPERIAL": "city_cl_210",
    "NUNOA": "city_cl_314",
    "OHIGGINS": "city_cl_280",
    "OLIVAR": "city_cl_93",
    "OLLAGUE": "city_cl_17",
    "OLMUE": "city_cl_70",
    "OSORNO": "city_cl_263",
    "OVALLE": "city_cl_40",
    "PADRE HURTADO": "city_cl_345",
    "PADRE LAS CASAS": "city_cl_211",
    "PAIHUANO": "city_cl_34",
    "PAILLACO": "city_cl_241",
    "PAINE": "city_cl_336",
    "PALENA": "city_cl_273",
    "PALMILLA": "city_cl_111",
    "PANGUIPULLI": "city_cl_242",
    "PANQUEHUE": "city_cl_80",
    "PAPUDO": "city_cl_61",
    "PAREDONES": "city_cl_105",
    "PARRAL": "city_cl_141",
    "PEDRO AGUIRRE CERDA": "city_cl_315",
    "PELARCO": "city_cl_121",
    "PELLUHUE": "city_cl_128",
    "PEMUCO": "city_cl_188",
    "PENAFLOR": "city_cl_346",
    "PENALOLEN": "city_cl_316",
    "PENCAHUE": "city_cl_122",
    "PENCO": "city_cl_152",
    "PERALILLO": "city_cl_112",
    "PERQUENCO": "city_cl_212",
    "PETORCA": "city_cl_62",
    "PEUMO": "city_cl_94",
    "PICA": "city_cl_09",
    "PICHIDEGUA": "city_cl_95",
    "PICHILEMU": "city_cl_100",
    "PINTO": "city_cl_189",
    "PIRQUE": "city_cl_328",
    "PITRUFQUEN": "city_cl_213",
    "PLACILLA": "city_cl_113",
    "PORTEZUELO": "city_cl_190",
    "PORVENIR": "city_cl_290",
    "POZO ALMONTE": "city_cl_10",
    "PRIMAVERA": "city_cl_291",
    "PROVIDENCIA": "city_cl_317",
    "PUCHUNCAVI": "city_cl_49",
    "PUCON": "city_cl_214",
    "PUDAHUEL": "city_cl_318",
    "PUENTE ALTO": "city_cl_327",
    "PUERTO MONTT": "city_cl_244",
    "PUERTO OCTAY": "city_cl_264",
    "PUERTO VARAS": "city_cl_252",
    "PUMANQUE": "city_cl_114",
    "PUNITAQUI": "city_cl_43",
    "PUNTA ARENAS": "city_cl_284",
    "PUQUELDON": "city_cl_258",
    "PUREN": "city_cl_228",
    "PURRANQUE": "city_cl_265",
    "PUTAENDO": "city_cl_81",
    "PUTRE": "city_cl_03",
    "PUYEHUE": "city_cl_266",
    "QUEILEN": "city_cl_259",
    "QUELLON": "city_cl_260",
    "QUEMCHI": "city_cl_261",
    "QUILACO": "city_cl_172",
    "QUILICURA": "city_cl_319",
    "QUILLECO": "city_cl_173",
    "QUILLON": "city_cl_191",
    "QUILLOTA": "city_cl_64",
    "QUILPUE": "city_cl_50",
    "QUINCHAO": "city_cl_262",
    "QUINTA DE TILCOCO": "city_cl_96",
    "QUINTA NORMAL": "city_cl_320",
    "QUINTERO": "city_cl_51",
    "QUIRIHUE": "city_cl_192",
    "RANCAGUA": "city_cl_83",
    "RANQUIL": "city_cl_193",
    "RAUCO": "city_cl_133",
    "RECOLETA": "city_cl_321",
    "RENAICO": "city_cl_229",
    "RENCA": "city_cl_322",
    "RENGO": "city_cl_97",
    "REQUINOA": "city_cl_98",
    "RETIRO": "city_cl_142",
    "RINCONADA": "city_cl_57",
    "RIO BUENO": "city_cl_243",
    "RIO CLARO": "city_cl_123",
    "RIO HURTADO": "city_cl_44",
    "RIO IBANEZ": "city_cl_283",
    "RIO NEGRO": "city_cl_267",
    "RIO VERDE": "city_cl_286",
    "ROMERAL": "city_cl_134",
    "SAAVEDRA": "city_cl_215",
    "SAGRADA FAMILIA": "city_cl_135",
    "SALAMANCA": "city_cl_39",
    "SAN ANTONIO": "city_cl_71",
    "SAN BERNARDO": "city_cl_333",
    "SAN CARLOS": "city_cl_194",
    "SAN CLEMENTE": "city_cl_124",
    "SAN ESTEBAN": "city_cl_58",
    "SAN FABIAN": "city_cl_195",
    "SAN FELIPE": "city_cl_77",
    "SAN FERNANDO": "city_cl_106",
    "SAN GREGORIO": "city_cl_287",
    "SAN IGNACIO": "city_cl_196",
    "SAN JAVIER": "city_cl_143",
    "SAN JOAQUIN": "city_cl_323",
    "SAN JOSE DE MAIPO": "city_cl_329",
    "SAN JUAN DE LA COSTA": "city_cl_268",
    "SAN MIGUEL": "city_cl_324",
    "SAN NICOLAS": "city_cl_197",
    "SAN PABLO": "city_cl_269",
    "SAN PEDRO": "city_cl_341",
    "SAN PEDRO DE ATACAMA": "city_cl_18",
    "SAN PEDRO DE LA PAZ": "city_cl_153",
    "SAN RAFAEL": "city_cl_125",
    "SAN RAMON": "city_cl_325",
    "SAN ROSENDO": "city_cl_174",
    "SAN VICENTE": "city_cl_99",
    "SANTA BARBARA": "city_cl_175",
    "SANTA CRUZ": "city_cl_115",
    "SANTA JUANA": "city_cl_154",
    "SANTA MARIA": "city_cl_82",
    "SANTIAGO": "city_cl_295",
    "SANTO DOMINGO": "city_cl_76",
    "SIERRA GORDA": "city_cl_14",
    "TALAGANTE": "city_cl_342",
    "TALCA": "city_cl_116",
    "TALCAHUANO": "city_cl_155",
    "TALTAL": "city_cl_15",
    "TEMUCO": "city_cl_200",
    "TENO": "city_cl_136",
    "TEODORO SCHMIDT": "city_cl_216",
    "TIERRA AMARILLA": "city_cl_23",
    "TIL TIL": "city_cl_332",
    "TIMAUKEL": "city_cl_292",
    "TIRUA": "city_cl_164",
    "TOCOPILLA": "city_cl_19",
    "TOLTEN": "city_cl_217",
    "TOME": "city_cl_156",
    "TORRES DEL PAINE": "city_cl_294",
    "TORTEL": "city_cl_281",
    "TRAIGUEN": "city_cl_230",
    "TREHUACO": "city_cl_198",
    "TUCAPEL": "city_cl_176",
    "VALDIVIA": "city_cl_232",
    "VALLENAR": "city_cl_26",
    "VALPARAISO": "city_cl_45",
    "VICHUQUEN": "city_cl_137",
    "VICTORIA": "city_cl_231",
    "VICUNA": "city_cl_35",
    "VILCUN": "city_cl_218",
    "VILLA ALEGRE": "city_cl_144",
    "VILLA ALEMANA": "city_cl_52",
    "VILLARRICA": "city_cl_219",
    "VINA DEL MAR": "city_cl_53",
    "VITACURA": "city_cl_326",
    "YERBAS BUENAS": "city_cl_145",
    "YUMBEL": "city_cl_177",
    "YUNGAY": "city_cl_199",
    "ZAPALLAR": "city_cl_63",
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
            _logger.error(f"DocumentosOnline: Error API para {endpoint}/{value}: {str(e)}, Respuesta: {getattr(e.response, 'text', 'No response')}")
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
        return self.env.ref(f'l10n_cl.{comuna_ref}').id if comuna_ref else False

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

        # Check if bmya_support_service is installed
        if self.env['ir.module.module'].search([
            ('name', '=', 'bmya_support_service'),
            ('state', '=', 'installed')
        ], limit=1):
            # Use token from bmya_support_service (company-level for multi-company support)
            # URL is always read from config_parameter (shared across companies)
            company = self.env.company
            url = conf.get_str('docsonline.url') or conf.get_str('bmya_support_service.url') or 'https://www.documentosonline.cl'
            token = company.docs_online_token_auth or conf.get_str('bmya_support_service.token') or conf.get_str('docsonline.token')
        else:
            # Fallback to config parameters (l10n_cl_docsonline_partner standalone)
            url = conf.get_str('docsonline.url') or 'https://www.documentosonline.cl'
            token = conf.get_str('docsonline.token')
        if not url or not token:
            raise UserError(_('DocsOnline: URL or token not configured'))
        return {
            'url': url,
            'token': token,
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
        if not rut_input and not self.vat:
            _logger.info("No RUT or name provided for DocsOnline query")
            return
        rut = rut_input or self.vat.replace('.', '')
        partner_values = self._fetch_docsonline_partner_data('partner/details', rut)
        if 'error' in partner_values:
            raise UserError(_('DocumentosOnline: %s') % partner_values['error'])
        if not partner_values.get('razon_social'):
            raise UserError(_('No se encontraron datos para el RUT %s. Intente buscar en www.documentosonline.cl') % rut)

        partner_odoo_data = self._prepare_single_partner_data(partner_values)
        config_params = self.env['ir.config_parameter'].sudo()

        update_vals = {
            'vat': partner_odoo_data.get('vat', rut),
            'l10n_cl_sii_taxpayer_type': partner_odoo_data['l10n_cl_sii_taxpayer_type'],
        }
        if config_params.get_bool('docsonline.replace_name'):
            update_vals['name'] = partner_odoo_data['name']
        if config_params.get_bool('docsonline.replace_street'):
            update_vals.update({
                'street': partner_odoo_data['street'],
                'street2': partner_odoo_data['street2'],
                'city': partner_odoo_data['city'],
                'city_id': partner_odoo_data['city_id'],
            })
        if config_params.get_bool('docsonline.replace_email') or not self.l10n_cl_dte_email:
            update_vals['l10n_cl_dte_email'] = partner_odoo_data['l10n_cl_dte_email']
        if config_params.get_bool('docsonline.replace_activity') or not self.l10n_cl_activity_description:
            update_vals['l10n_cl_activity_description'] = partner_odoo_data['l10n_cl_activity_description']

        self.update(update_vals)

    def press_to_update(self):
        """Update partner data from DocsOnline when the update button is pressed."""
        if not self.vat and not self.name:
            raise UserError(_('Se requiere el RUT o el Nombre para actualizar desde DocumentosOnline'))
        rut_input = (self.vat or self.name).replace('.', '')
        self._get_data_from_docsonline(rut_input)

    def multiple_update(self):
        """Update multiple partners from DocsOnline data."""
        for r in self:
            try:
                if r.country_code != 'CL':
                    msg = _('La Empresa %(name)s no se actualizó: no es de Chile') % {'name': r.name}
                    r._send_notification('warning', msg, sticky=False)
                    continue
                if not r.is_company and r.parent_id:
                    msg = _('El contacto %(name)s no se actualizó: es un contacto de %(parent)s') % {
                        'name': r.name,
                        'parent': r.commercial_partner_id.name
                    }
                    r._send_notification('danger', msg, sticky=True)
                    continue
                if r.is_company and r.parent_id:
                    msg = _('La empresa %(name)s no se actualizó: es una sucursal de of %(parent)s') % {
                        'name': r.name,
                        'parent': r.commercial_partner_id.name
                    }
                    r._send_notification('warning', msg, sticky=False)
                    continue
                r.press_to_update()
                msg = _('La empresa %(name)s se actualizó con éxito') % {'name': r.name}
                r._send_notification('info', msg, sticky=False)
                _logger.info(msg)
            except Exception as e:
                msg = _('Falló la actualización de la empresa %(name)s: %(error)s') % {
                    'name': r.name,
                    'error': str(e)
                }
                r._send_notification('warning', msg, sticky=True)
                _logger.warning(msg)
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
