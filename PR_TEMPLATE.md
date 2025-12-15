# Migración a Odoo 19.0 - odoo-bmya

## Resumen
Migración de 16 módulos community/LGPL-3 de odoo-bmya desde Odoo 18.0 a Odoo 19.0.

## Cambios Realizados

### 📦 Manifests Actualizados (16 módulos)
Todos los módulos actualizados de `18.0.x.x.x` → `19.0.1.0.0`.

**Módulos migrados:**
- account_move_change_currency
- auth_server_admin_passwd_passkey
- l10n_cl_counties (346 comunas chilenas)
- l10n_cl_counties_as_region
- l10n_cl_default_document_type
- l10n_cl_docsonline_partner
- l10n_cl_edi_fix_validation
- l10n_cl_edi_qbli
- l10n_cl_edi_special_fields
- l10n_cl_edi_stock_special_fields
- l10n_cl_partner_extra_xml_identification
- l10n_cl_report_invoice_cedible
- l10n_latam_default_document
- picking_from_xls
- purchase_order_report
- sale_order_report

### 🐍 Código Python Actualizado (1 archivo)

**account_move_change_currency/wizard/account_change_currency.py**
- Línea 36: `self._context.get('active_id')` → `self.env.context.get('active_id')`
- Corrección en método `_get_move()` para obtener factura del contexto

## Testing Requerido

### ✅ Funcionalidad Crítica a Validar

#### Localización Chilena
- [ ] `l10n_cl_counties`: Selector de 346 comunas en partners
- [ ] `l10n_cl_default_document_type`: Tipo documento automático por contribuyente
- [ ] `l10n_cl_docsonline_partner`: Obtener datos desde DocsOnline

#### Reportes Chilenos
- [ ] `purchase_order_report`: Formato chileno (recuadro margen superior)
- [ ] `sale_order_report`: Formato chileno (recuadro margen superior)
- [ ] `l10n_cl_report_invoice_cedible`: Factura cedible separada

#### EDI Especial
- [ ] `l10n_cl_edi_qbli`: Código SAP en XML
- [ ] `l10n_cl_edi_special_fields`: Asignación a empresa principal
- [ ] `l10n_cl_edi_fix_validation`: Validaciones obligatorias

#### Utilidades
- [ ] `account_move_change_currency`: Cambio de moneda en facturas
- [ ] `picking_from_xls`: Importar picking desde Excel

### 🧪 Comandos de Testing

```bash
# Testing de localización chilena
odoo-bin -c odoo.conf -d test_db -i l10n_cl_counties,l10n_cl_default_document_type --test-enable

# Testing de reportes
odoo-bin -c odoo.conf -d test_db -i purchase_order_report,sale_order_report --test-enable

# Testing completo
odoo-bin -c odoo.conf -d test_db -u all --test-enable --stop-after-init
```

## Compatibilidad

- **Odoo Version:** 19.0
- **Python:** 3.10+
- **License:** LGPL-3 (community modules)
- **Dependencias externas:** Sin cambios
- **Breaking changes:** Solo API deprecations (corregidas)

## Notas Adicionales

- **l10n_cl_counties** es fundamental: contiene 346 comunas oficiales de Chile
- Los reportes están adaptados al formato estándar chileno
- Módulos compatibles con localización oficial l10n_cl

## Checklist de Revisión

- [x] Manifests actualizados a 19.0.1.0.0
- [x] Código Python corregido para Odoo 19
- [x] Commit message con formato estándar
- [ ] Testing manual completado
- [ ] Validar selector de comunas
- [ ] Validar formato reportes chilenos
- [ ] Aprobación de QA
- [ ] Ready to merge

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
