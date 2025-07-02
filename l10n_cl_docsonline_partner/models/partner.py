# -*- coding: utf-8 -*-
import json
import logging
import requests
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

class ResPartner(models.Model):
    _inherit = 'res.partner'

    backup_name = fields.Char('Backup Name')

    def _fetch_docsonline_partner_data(self, endpoint, value):
        """Fetch data from DocsOnline API for a given endpoint and value.
        Args:
            endpoint (str): API endpoint to call (e.g., 'partner/search', 'partner/details').
            value (str): Value to pass to the endpoint (e.g., RUT or search term).
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
            response = requests.get(
                f"{docsonline_data['url']}/{endpoint}/{value}",
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
        except requests.RequestException as e:
            _logger.error("DocsumentosOnline: Error API para %s/%s: %s, Respuesta: %s", endpoint, value, str(e), getattr(e.response, 'text', 'No response'))
            try:
                error_detail = e.response.json().get('detail', str(e))  # Extract detail from JSON response
                raise UserError(_('DocumentosOnline: %s') % error_detail)
            except (json.JSONDecodeError, AttributeError):
                raise UserError(_('DocumentosOnline: %s') % str(e))  # Fallback to generic error
        try:
            data = response.json()
            _logger.debug("DocumentosOnline: %s/%s: %s", endpoint, value, data)
            return data
        except json.JSONDecodeError:
            _logger.error("Invalid JSON response for %s/%s: %s", endpoint, value, response.text)
            raise UserError(_('DocsOnline: Invalid response format'))

    def _process_dol_data(self, partner_values):
        list_partner_data = []
        for key, list_data in partner_values.items():
            for data in list_data:
                partner_odoo_data = self._prepare_data_entry(data, is_branch=False, for_wizard=True)
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

    def _prepare_data_entry(self, data, is_branch=False, for_wizard=False):
        address_data = data.get('contacto', {})
        city = self._capital_preferences(address_data.get('comuna', ''))

        if for_wizard:
            # Wizard-specific fields only
            base_data = {
                'name': self._capital_preferences(data.get('razon_social', False)),
                'vat': data.get('rut', ''),
                'street': self._capital_preferences(
                    f"{address_data.get('calle', '')} {address_data.get('numero', '')} "
                    f"{address_data.get('departamento', '')} {address_data.get('bloque', '')}"
                ).strip(),
                'city': city,
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
                'city': city,
                'city_id': self._get_partner_location_id(city),
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

    def call_wizard(self):
        """Launch a wizard to select a partner from DocsOnline data.

        Returns:
            dict: Action dictionary to open the wizard.
        """
        self.ensure_one()
        partner_values = self._fetch_docsonline_partner_data('partner/search', self.name)
        wizard_obj = self.env['res.partner.docs.online']
        wizard_obj_data = self.env['res.partner.docs.online.data']
        wizard_obj.truncate()
        wizard_obj_data.truncate()
        wizard_id = wizard_obj.create({'partner_id': self.id})
        list_partner_data = self._process_dol_data(partner_values)
        for partner_odoo_data in list_partner_data:
            _logger.info("Creating wizard data: %s", partner_odoo_data)
            wizard_obj_data.create(partner_odoo_data)

        return {
            'type': 'ir.actions.act_window',
            'name': _('Select a partner from a list'),
            'res_model': 'res.partner.docs.online',
            'view_mode': 'form',
            'view_type': 'form',
            'view_id': self.env.ref('l10n_cl_docsonline_partner.tree_docsonline_partners_view').id,
            'target': 'new',
            'active_id': wizard_id.id,
            'res_id': wizard_id.id,
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
            _logger.warning("DocsOnline error: %s", partner_values['error'])
            raise UserError(_('No data found on www.documentosonline.cl: %s') % partner_values.get('error'))
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
                'city': self._capital_preferences(branch.get('comuna', '')),
                'city_id': self._get_partner_location_id(self._capital_preferences(branch.get('comuna', ''))),
                'state_id': self._get_partner_state_id(branch.get('region', None)),
                'country_id': self.env.ref('base.cl').id,
                'type': 'other',
            })
        return branch_data