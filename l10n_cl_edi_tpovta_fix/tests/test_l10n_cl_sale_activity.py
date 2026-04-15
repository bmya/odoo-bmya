from unittest.mock import MagicMock, patch
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestL10nClSaleActivity(TransactionCase):
    """Tests para _l10n_cl_sale_activity() en account.move.

    Verifica que el método retorne el código correcto de TpoTranVenta según
    el tipo de cuenta contable utilizada en las líneas de la factura:
      1 → ventas del giro (por defecto)
      2 → ventas de activo fijo
      3 → otras ventas
    """

    def _make_read_group_result(self, account_types):
        mock_account = MagicMock()
        mock_account.mapped.return_value = account_types
        return [(mock_account,)]

    def test_sale_activity_returns_1_for_regular_income(self):
        move = self.env['account.move'].new({'move_type': 'out_invoice'})
        with patch.object(
            type(self.env['account.move.line']), '_read_group',
            return_value=self._make_read_group_result(['income'])
        ):
            self.assertEqual(move._l10n_cl_sale_activity(), 1)

    def test_sale_activity_returns_2_for_fixed_asset(self):
        move = self.env['account.move'].new({'move_type': 'out_invoice'})
        with patch.object(
            type(self.env['account.move.line']), '_read_group',
            return_value=self._make_read_group_result(['asset_fixed'])
        ):
            self.assertEqual(move._l10n_cl_sale_activity(), 2)

    def test_sale_activity_returns_3_for_other_income(self):
        move = self.env['account.move'].new({'move_type': 'out_invoice'})
        with patch.object(
            type(self.env['account.move.line']), '_read_group',
            return_value=self._make_read_group_result(['income_other'])
        ):
            self.assertEqual(move._l10n_cl_sale_activity(), 3)
