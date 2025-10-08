import json
import logging
import time
import urllib

import requests
from odoo.exceptions import UserError

from odoo import _, api, fields, models

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

class PartnerDataSII(models.Model):
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
            _logger.debug("DocsOnline response for %s/%s: %s", endpoint, value, data)
            return data
        except json.JSONDecodeError:
            _logger.error("Invalid JSON response for %s/%s: %s", endpoint, value, response.text)
            raise UserError(_('DocsOnline: Invalid response format'))

    def _process_dol_data(self, partner_values):
        list_partner_data = []
        for key, list_data in partner_values.items():
            for data in list_data:
                partner_odoo_data = self._prepare_data_entry(data, is_branch=False)
                list_partner_data.append(partner_odoo_data)
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
            city (str): Name of the city to search for.

        Returns:
            int: ID of the city if found, False otherwise.
        """
        if not city:
            return False
        comuna = self.env['res.city'].search([('name', '=', city.title())], limit=1)
        return comuna.id if comuna else False

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

    def _prepare_data_entry(self, data, is_branch=False, parent_id=None, for_wizard=False):
        address_data = data.get('contacto', {})
        # Prepare base data common to all cases
        city = self._capital_preferences(address_data.get('comuna', ''))
        base_data = {
            'name': self._capital_preferences(data.get('razon_social', False)),
            'vat': data.get('rut', ''),
            'city': city,
            'l10n_cl_activity_description': self._capital_preferences(data.get('giro', '')),
        }

        # Add address fields with or without street2 separation based on context
        if for_wizard:
            base_data['street'] = self._capital_preferences(
                f"{address_data.get('calle', '')} {address_data.get('numero', '')} "
                f"{address_data.get('departamento', '')} {address_data.get('bloque', '')}"
            ).strip()
        else:
            base_data['street'] = self._capital_preferences(
                f"{address_data.get('calle', '')} {address_data.get('numero', '')}"
            ).strip()
            base_data['street2'] = self._capital_preferences(
                f"{address_data.get('departamento', '')} {address_data.get('bloque', '')}"
            ).strip()
            base_data['city_id'] = self._get_partner_location_id(city)
            base_data['state_id'] = self._get_partner_state_id(address_data.get('region', None))
            base_data['country_id'] = self.env.ref('base.cl').id

        if is_branch and parent_id:
            # Branch-specific data
            return {
                'parent_id': parent_id.id,
                'name': self._capital_preferences(
                    f"{parent_id.name} - SUC: {address_data.get('calle', '')} {address_data.get('numero', '')}"
                ),
                'street': base_data['street'],
                'street2': base_data['street2'],
                'city': base_data['city'],
                'city_id': base_data['city_id'],
                'state_id': base_data['state_id'],
                'country_id': base_data['country_id'],
                'type': 'other',
            }
        elif not for_wizard:
            # Detailed data for a single partner (not wizard)
            base_data.update({
                'l10n_latam_identification_type_id': self.env.ref('l10n_cl.it_RUT').id,
                'l10n_cl_sii_taxpayer_type': '1',
                'l10n_cl_dte_email': data.get('email_intercambio', ''),
            })
        return base_data

    def _prepare_single_partner_data(self, partner_values):
        return self._prepare_data_entry(partner_values, is_branch=False, for_wizard=False)

    def _process_dol_data(self, partner_values):
        """Process multiple partner data entries from DocsOnline API response for the wizard.

        Args:
            partner_values (dict): Dictionary with lists of partner data entries.

        Returns:
            list: List of processed partner data dictionaries.
        """
        list_partner_data = []
        for key, list_data in partner_values.items():
            for data in list_data:
                partner_odoo_data = self._prepare_data_entry(data, is_branch=False, for_wizard=True)
                list_partner_data.append(partner_odoo_data)
        return list_partner_data

    def _get_docsonline_data(self):
        """Get configuration data for DocsOnline API.

        Returns:
            dict: Dictionary with API URL and token.
        """
        conf = self.env['ir.config_parameter'].sudo()
        return {
            'url': conf.get_param('docsonline.url', 'https://www.documentosonline.cl'),
            'token': conf.get_param('docsonline.token'),
        }

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
