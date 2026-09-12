from odoo import models

# Código SII del IVA, igual que en l10n_cl_edi_stock
TAX19_SII_CODE = 14


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def _l10n_cl_prepare_tax_base_lines(self):
        """Arma las base lines de la guía de despacho.

        Replica el criterio con el que `_l10n_cl_get_tax_amounts` de
        `l10n_cl_edi_stock` elige impuestos, precio y cantidad de cada movimiento
        (precio de lista del producto o precio de la orden de venta, según
        `l10n_cl_delivery_guide_price` del cliente). Al migrar de versión hay que
        comparar este método contra el original.
        """
        self.ensure_one()
        account_tax = self.env['account.tax']
        company = self.company_id
        guide_price = self.partner_id.l10n_cl_delivery_guide_price
        if guide_price == 'none':
            return []
        # Sin soporte para monedas extranjeras: se cae al precio del producto
        if guide_price == 'sale_order' and (
                not self.sale_id or self.sale_id.currency_id != company.currency_id):
            guide_price = 'product'

        base_lines = []
        for move in self.move_ids.filtered(lambda x: x.quantity > 0):
            sale_line = move.sale_line_id
            # Los componentes de un kit apuntan a la línea de venta del kit: se
            # valorizan por su propio producto para evitar conversiones de UoM
            move_guide_price = 'product' if sale_line and move.product_id != sale_line.product_id else guide_price
            if move_guide_price == 'product' or not sale_line:
                taxes = move.product_id.taxes_id.filtered(lambda t: t.company_id == company)
                price = move.product_id.lst_price
                quantity = move.quantity
                uom = move.product_uom
            else:
                taxes = sale_line.tax_ids
                quantity = move.product_uom._compute_quantity(move.quantity, sale_line.product_uom_id)
                price = sale_line.price_unit * (1 - (sale_line.discount or 0.0) / 100.0)
                uom = sale_line.product_uom_id
            base_lines.append(account_tax._prepare_base_line_for_taxes_computation(
                move,
                partner_id=self.partner_id,
                currency_id=company.currency_id,
                product_id=move.product_id,
                product_uom_id=uom,
                tax_ids=taxes,
                price_unit=price,
                quantity=quantity,
            ))
        return base_lines

    def _l10n_cl_get_tax_amounts(self):
        """Recalcula los totales de la guía con el método de redondeo de la compañía.

        El método original llama a `account.tax.compute_all()` una vez por movimiento y
        suma los resultados, y `compute_all()` redondea el importe de impuesto de cada
        llamada a la moneda. Con eso el redondeo de cada línea se acumula en los totales
        aunque la compañía esté configurada para redondear globalmente: en pesos chilenos
        una guía de varias líneas informa un IVA unos pesos mayor al de la orden de venta
        y al de la factura, que sí redondean globalmente.

        Acá se rehace el cálculo con todos los movimientos juntos, usando los mismos
        helpers que usan la orden de venta y la factura, para que los tres documentos
        informen el mismo IVA. Los deltas de redondeo del neto se reparten entre las
        líneas, igual que en la factura, así la suma de los `MontoItem` sigue coincidiendo
        con el `MntNeto` del encabezado.
        """
        totals, retentions, line_amounts = super()._l10n_cl_get_tax_amounts()
        if not line_amounts or self.company_id.tax_calculation_rounding_method != 'round_globally':
            return totals, retentions, line_amounts

        base_lines = self._l10n_cl_prepare_tax_base_lines()
        if not base_lines:
            return totals, retentions, line_amounts

        account_tax = self.env['account.tax']
        account_tax._add_tax_details_in_base_lines(base_lines, self.company_id)
        account_tax._round_base_lines_tax_details(base_lines, self.company_id)

        chart_template = self.env['account.chart.template'].with_company(self.company_id)
        retention_groups = set()
        for group_xmlid in ('tax_group_ila', 'tax_group_retenciones'):
            group = chart_template.ref(group_xmlid, raise_if_not_found=False)
            if group:
                retention_groups.add(group.id)

        totals.update({
            'vat_amount': 0.0,
            'subtotal_amount_taxable': 0.0,
            'subtotal_amount_exempt': 0.0,
            'total_amount': 0.0,
        })
        new_retentions = {}
        for base_line in base_lines:
            move = base_line['record']
            tax_details = base_line['tax_details']
            # El delta del neto lo asigna `_round_base_lines_tax_details` a una línea
            delta = tax_details['delta_total_excluded_currency']
            net_amount = tax_details['total_excluded_currency'] + delta
            # el total con impuestos se rearma acá: el `total_included_currency` que deja
            # `_round_base_lines_tax_details` se calcula antes de repartir los deltas
            tax_amount = 0.0
            has_vat = False
            for tax_data in tax_details['taxes_data']:
                tax = tax_data['tax']
                tax_amount += tax_data['tax_amount_currency']
                if tax.l10n_cl_sii_code == TAX19_SII_CODE:
                    has_vat = True
                    totals['vat_amount'] += tax_data['tax_amount_currency']
                elif tax.tax_group_id.id in retention_groups:
                    key = (tax.l10n_cl_sii_code, tax.amount, tax.tax_group_id.name)
                    new_retentions.setdefault(key, 0.0)
                    new_retentions[key] += tax_data['tax_amount_currency']
            if has_vat:
                totals['subtotal_amount_taxable'] += net_amount
            else:
                totals['subtotal_amount_exempt'] += net_amount
            totals['total_amount'] += net_amount + tax_amount

            if move in line_amounts:
                line_amounts[move].update({
                    'total_amount': net_amount,
                    'value': net_amount + tax_amount,
                })

        for retention in retentions:
            key = (retention['tax_code'], retention['tax_percent'], retention['tax_name'])
            if key in new_retentions:
                retention['tax_amount'] = self.company_id.currency_id.round(new_retentions[key])
        return totals, retentions, line_amounts
