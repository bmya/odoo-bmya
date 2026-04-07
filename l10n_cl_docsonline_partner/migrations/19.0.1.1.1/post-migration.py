def migrate(cr, version):
    """Force update partner_view.xml for migrated databases.

    In databases migrated from v18 to v19, views may not update automatically.
    This script forces the view to reload from XML by clearing arch_base.
    """
    if not version:
        return

    # Force reload of partner form view
    cr.execute("""
        UPDATE ir_ui_view
        SET arch_base = NULL
        WHERE id IN (
            SELECT res_id FROM ir_model_data
            WHERE module = 'l10n_cl_docsonline_partner'
            AND name = 'view_update_button_form'
            AND model = 'ir.ui.view'
        )
    """)