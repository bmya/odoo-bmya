from unittest.mock import patch

import requests

from odoo.tests import TransactionCase, tagged

DOCSONLINE_URL = 'https://www.documentosonline.cl/api/mindicador/tc_TestKey123'


class FakeResponse:
    def __init__(self, payload=None, status=200):
        self.payload = payload
        self.status_code = status
        self.text = '{}'

    def raise_for_status(self):
        if self.status_code >= 400:
            error = requests.HTTPError('%s Error for url: %s' % (self.status_code, DOCSONLINE_URL))
            error.response = self
            raise error

    def json(self):
        return self.payload


def serie(codigo, fecha, valor):
    return FakeResponse({'codigo': codigo, 'serie': [{'fecha': '%sT03:00:00.000Z' % fecha, 'valor': valor}]})


@tagged('post_install', '-at_install')
class TestParseMindicadorYuan(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env['ir.config_parameter'].sudo().set_param('mindicador_api_url', DOCSONLINE_URL)
        cls.currencies = cls.env['res.currency'].with_context(active_test=False).search(
            [('name', 'in', ['USD', 'CNY'])])
        cls.currencies.active = True

    def _parse(self, currencies, yuan_response=None):
        requested = []

        def fake_get(url, timeout=None):
            requested.append(url)
            if '/yuan/' in url:
                return yuan_response or serie('yuan', '2026-11-23', 152.39)
            return serie('dolar', '2026-11-23', 1017.17)

        with patch.object(requests, 'get', side_effect=fake_get):
            rslt = self.env.company._parse_mindicador_data(currencies)
        return rslt, requested

    def test_cny_is_requested_from_docsonline(self):
        rslt, requested = self._parse(self.currencies)
        self.assertAlmostEqual(rslt['CNY'][0], 1.0 / 152.39)
        self.assertEqual(rslt['CNY'][1], '2026-11-23')
        self.assertIn('USD', rslt)
        yuan_urls = [url for url in requested if '/yuan/' in url]
        self.assertEqual(len(yuan_urls), 1)
        self.assertTrue(yuan_urls[0].startswith(DOCSONLINE_URL + '/yuan/'))

    def test_inactive_cny_is_not_requested(self):
        rslt, requested = self._parse(self.currencies.filtered(lambda c: c.name == 'USD'))
        self.assertNotIn('CNY', rslt)
        self.assertFalse([url for url in requested if '/yuan/' in url])

    def test_mindicador_cl_url_does_not_request_cny(self):
        self.env['ir.config_parameter'].sudo().set_param('mindicador_api_url', 'https://mindicador.cl/api')
        rslt, requested = self._parse(self.currencies)
        self.assertNotIn('CNY', rslt)
        self.assertIn('USD', rslt)
        self.assertFalse([url for url in requested if '/yuan/' in url])

    def test_cny_error_keeps_other_currencies(self):
        with self.assertLogs('odoo.addons.docsonline_currency_rate_yuan.models.res_company', 'WARNING') as logs:
            rslt, _requested = self._parse(self.currencies, yuan_response=FakeResponse(status=503))
        self.assertNotIn('CNY', rslt)
        self.assertIn('USD', rslt)
        self.assertIn('HTTP 503', logs.output[0])
        self.assertNotIn('tc_TestKey123', logs.output[0])

    def test_empty_serie_is_skipped(self):
        rslt, _requested = self._parse(self.currencies, yuan_response=FakeResponse({'serie': []}))
        self.assertNotIn('CNY', rslt)
        self.assertIn('USD', rslt)
