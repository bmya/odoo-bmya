# Módulos retirados de 20.0

Estos módulos **no se migran a Odoo 20.0** y se quitaron de esta rama. Siguen en las ramas
anteriores (16.0–19.0) para los clientes que los tengan instalados.

- **Antes de pasar un cliente a 20.0:** desinstalarlos en su base, sobre la versión que use
  hoy, como indica la última columna. Si quedan instalados, el upgrade los encuentra sin
  código.
- **Forward-port:** si un PR a 19.0 toca uno de estos módulos, se mergea con
  `@robbmya r+ no-fw`. Si no, el forward-port a 20.0 choca contra el borrado.
- La decisión es parte del plan de migración de módulos BMyA a 20.0 (2026-09-27).

| Módulo | Por qué se retira | Qué usar en 20.0 | Antes del upgrade del cliente |
|---|---|---|---|
| `auth_server_admin_passwd_passkey` | Roto desde antes de 19.0 (sobrescribe `check_credentials`, que ya no existe) y no instalable en 16.0–19.0. Además es un riesgo de seguridad | `bmya_support_connect_as` (bmya-enterprise): token de un solo uso, con auditoría | Desinstalar |
| `picking_from_xls` | Escribe `move_ids_without_package`, que ya no existe, y depende de `xlrd` (solo `.xls`). No es instalable desde 17.0 | Importar las operaciones de la transferencia con **Importar registros** (`base_import`) | Desinstalar |
| `l10n_cl_counties_as_region` | Sin uso. Duplicaba las comunas como regiones para usar reglas de despacho por comuna | Las comunas nativas en `res.city` (`l10n_cl/data/res.city.csv`, 346 comunas), que `l10n_cl_counties` ya adopta en 20.0 | Desinstalar. **Borra los `res.country.state` que creó**: revisar antes las direcciones que los usen |
