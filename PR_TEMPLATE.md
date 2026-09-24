# [MIG] <modulo>: migración a 20.0 - odoo-bmya

<!--
Un PR por módulo contra `20.0`, en el orden de dependencias del checklist del
PR [INIT]. La migración 18.0 → 19.0 de este repo está documentada en el
PR_TEMPLATE.md de la rama 19.0.
-->

## Resumen
Migración de `<modulo>` de Odoo 19.0 a Odoo 20.0.

## Cambios
- [ ] `'installable': True` (el [INIT] dejó todos los módulos en `False`)
- [ ] Versión en `20.0.1.0.0`: la puso el [INIT]; subirla solo si el PR agrega un script de migración
- [ ] Código adaptado a la API de Odoo 20 (detallar)
- [ ] Vistas, assets y reportes adaptados (detallar)
- [ ] Scripts en `migrations/20.0.1.0.0/` si cambian modelos o datos existentes

## Pruebas
- [ ] Instala en una base nueva del entorno o20 (`-i <modulo> --stop-after-init`)
- [ ] Tests del módulo (`--test-enable --test-tags /<modulo>`)
- [ ] Build de runboat en verde (cuando runboat 20.0 esté habilitado)

## Forward-ports
- [ ] Incluidos los cambios de 19.0 posteriores a la creación de 20.0 que tocan este módulo (FW de 19.0 → 20.0)

## Compatibilidad
- **Odoo Version:** 20.0
- **Python:** 3.12+

## Checklist de Revisión
- [ ] Un solo commit `[MIG] <modulo>: migración a 20.0` (ci/commits)
- [ ] `ci/*` y `legal/cla` en verde
- [ ] Probado en el entorno o20
