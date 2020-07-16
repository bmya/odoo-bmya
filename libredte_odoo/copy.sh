#rsync -aruvz --dry-run --exclude={.git*,.idea,*.pyc} /opt/odoo/test-addons/odoo-chile/l10n_cl_dte/ /opt/odoo/test-addons/odoo-chile/libredte_odoo/l10n_cl_dte/
rsync -aruvz --exclude={.git*,.idea,*.pyc} /opt/odoo/test-addons/odoo-chile/l10n_cl_dte/ /opt/odoo/test-addons/odoo-chile/libredte_odoo/l10n_cl_dte/

