import logging

import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)

# Ruta del servicio de tasas de cambio de Docs Online. mindicador.cl no publica
# el yuan: con su URL, pedirlo daría 404 y rompería la actualización completa.
DOCSONLINE_PATH = '/api/mindicador/'


class ResCompany(models.Model):
    _inherit = 'res.company'

    def _parse_mindicador_data(self, available_currencies):
        """Agrega CNY a las tasas del proveedor mindicador.

        El método original recorre una lista fija (USD, EUR, UF, UTM). Aquí se
        pide el yuan con la misma forma (``{mindicador_api_url}/yuan/DD-MM-YYYY``)
        solo si CNY está activo y la URL es la de Docs Online.
        """
        rslt = super()._parse_mindicador_data(available_currencies)
        if 'CNY' not in available_currencies.mapped('name'):
            return rslt

        icp = self.env['ir.config_parameter'].sudo()
        server_url = icp.get_param('mindicador_api_url') or ''
        if DOCSONLINE_PATH not in server_url:
            _logger.debug('mindicador: CNY activo, pero mindicador_api_url no apunta a Docs Online.')
            return rslt

        timeout = int(icp.get_param('mindicador_api_timeout', 30))
        today_date = fields.Date.context_today(self.with_context(tz='America/Santiago'))
        url = '%s/yuan/%s' % (server_url.rstrip('/'), today_date.strftime('%d-%m-%Y'))
        try:
            res = requests.get(url, timeout=timeout)
            res.raise_for_status()
            serie = res.json()['serie']
            if serie:
                rslt['CNY'] = (1.0 / serie[0]['valor'], serie[0]['fecha'][:10])
        except (requests.RequestException, ValueError, KeyError, IndexError, TypeError, ZeroDivisionError) as error:
            # La URL lleva la key del cliente: no se registra, solo la causa.
            status = getattr(getattr(error, 'response', None), 'status_code', None)
            _logger.warning(
                'mindicador: no se pudo obtener la tasa CNY desde Docs Online (%s%s). '
                'Las demás monedas se actualizan igual.',
                type(error).__name__, ', HTTP %s' % status if status else '',
            )
        return rslt
