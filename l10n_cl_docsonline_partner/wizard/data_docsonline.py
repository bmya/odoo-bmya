import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class PartnerDocumentsOnline(models.TransientModel):
    _name = 'res.partner.docs.online'
    _description = 'DocsOnline Wizard'

    partner_id = fields.Many2one('res.partner', string='Partner')
    name = fields.Char(string='Name', related='partner_id.name', readonly=True)
    docs_online_data_ids = fields.Many2many('res.partner.docs.online.data', string='')

    @api.model
    def truncate(self):
        """Clear existing wizard data."""
        self.env.cr.execute('TRUNCATE res_partner_docs_online CASCADE')

    def _fetch_docsonline_partner_data(self, rut, include_branches=False):
        """Fetch partner data from DocsOnline API with optional branches.

        Args:
            rut (str): RUT of the partner to fetch data for.
            include_branches (bool): If True, include branch data in the API call.

        Returns:
            dict: JSON data from the API response.

        Raises:
            UserError: If the API call fails or the response is invalid.
        """
        partner_obj = self.env['res.partner']
        return partner_obj._fetch_docsonline_partner_data('partner/details', rut, include_sucursales=include_branches)

    def _update_partner_from_data(self, partner_data, protect_fields=False, update_vat=True):
        """Update the partner with data fetched from DocsOnline.

        Args:
            partner_data (dict): Data to update the partner with.
            protect_fields (bool): If True, respect configuration settings to protect certain fields.
            update_vat (bool): If True, update the VAT field.
        """
        partner_odoo_data = self.env['res.partner']._prepare_single_partner_data(partner_data)
        if update_vat:
            partner_odoo_data['vat'] = self.docs_online_data_ids[0].vat

        if protect_fields:
            config_params = self.env['ir.config_parameter'].sudo()
            update_vals = {
                'vat': partner_odoo_data['vat'],
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
            if config_params.get_param('docsonline.replace_email', False):
                update_vals['l10n_cl_dte_email'] = partner_odoo_data['l10n_cl_dte_email']
            if config_params.get_param('docsonline.replace_activity', False):
                update_vals['l10n_cl_activity_description'] = partner_odoo_data['l10n_cl_activity_description']
            self.partner_id.update(update_vals)
        else:
            self.partner_id.update(partner_odoo_data)

    def pick_partner(self):
        """Create or update a partner record from DocsOnline data without protected fields."""
        self.ensure_one()
        if not self.docs_online_data_ids:
            raise UserError(_("Por favor, seleccione un socio de la lista antes de confirmar."))
        nr = self.docs_online_data_ids[0]
        partner_values = self._fetch_docsonline_partner_data(nr.vat)
        self._update_partner_from_data(partner_values, protect_fields=False)

    def pick_partner_with_branches(self):
        """Create or update a partner record from DocsOnline data including branches."""
        self.ensure_one()
        if not self.docs_online_data_ids:
            raise UserError(_("Por favor, seleccione un socio de la lista antes de confirmar."))
        nr = self.docs_online_data_ids[0]
        partner_values = self._fetch_docsonline_partner_data(nr.vat, include_branches=True)
        self._update_partner_from_data(partner_values, protect_fields=False)
        branches = partner_values.get('domicilios', [])
        branches_odoo = self.env['res.partner']._prepare_branch_data(self.partner_id, branches)
        self.env['res.partner'].create(branches_odoo)
        # Se restaura la definición de la variable suc_qty
        suc_qty = len(branches_odoo)
        if suc_qty:
            _logger.info("Created %s branches for partner %s", suc_qty, self.partner_id.name)

    def pick_partner_protect(self):
        """Update existing partner record based on configuration settings for protected fields."""
        self.ensure_one()
        if not self.docs_online_data_ids:
            raise UserError(_("Por favor, seleccione un socio de la lista antes de confirmar."))
        nr = self.docs_online_data_ids[0]
        partner_values = self._fetch_docsonline_partner_data(nr.vat)
        self._update_partner_from_data(partner_values, protect_fields=True)

class PartnerDocumentsOnLineData(models.TransientModel):
    _name = 'res.partner.docs.online.data'
    _description = 'DocsOnline Wizard Data'

    partner_docs_ids = fields.Many2many('res.partner.docs.online', string='Lines')
    name = fields.Char('Name')
    display_name = fields.Char("List Name", compute='_compute_display_name')
    street = fields.Char('Street')
    city = fields.Char('City')
    vat = fields.Char('RUT')
    l10n_cl_activity_description = fields.Char(string='Activity Description')

    @api.model
    def truncate(self):
        """Clear existing wizard data."""
        self.env.cr.execute('TRUNCATE res_partner_docs_online_data CASCADE')

    @api.depends('name', 'vat', 'street', 'l10n_cl_activity_description')
    def _compute_display_name(self):
        for record in self:
            name_parts = [part for part in [
                record.name,
                record.vat,
                record.street,
                record.l10n_cl_activity_description
            ] if part]
            record.display_name = ' - '.join(name_parts) if name_parts else f"{record._name},{record.id}"
