from odoo.upgrade import util

RES_COUNTRY_STATES = [
    ('l10n_cl_counties.state_cl_011', 'base.state_cl_01'),
    ('l10n_cl_counties.state_cl_014', 'base.state_cl_01'),
    ('l10n_cl_counties.state_cl_021', 'base.state_cl_02'),
    ('l10n_cl_counties.state_cl_022', 'base.state_cl_02'),
    ('l10n_cl_counties.state_cl_023', 'base.state_cl_02'),
    ('l10n_cl_counties.state_cl_031', 'base.state_cl_03'),
    ('l10n_cl_counties.state_cl_032', 'base.state_cl_03'),
    ('l10n_cl_counties.state_cl_033', 'base.state_cl_03'),
    ('l10n_cl_counties.state_cl_041', 'base.state_cl_04'),
    ('l10n_cl_counties.state_cl_042', 'base.state_cl_04'),
    ('l10n_cl_counties.state_cl_043', 'base.state_cl_04'),
    ('l10n_cl_counties.state_cl_051', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_052', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_053', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_054', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_055', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_056', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_057', 'base.state_cl_05'),
    ('l10n_cl_counties.state_cl_061', 'base.state_cl_06'),
    ('l10n_cl_counties.state_cl_062', 'base.state_cl_06'),
    ('l10n_cl_counties.state_cl_063', 'base.state_cl_06'),
    ('l10n_cl_counties.state_cl_071', 'base.state_cl_07'),
    ('l10n_cl_counties.state_cl_072', 'base.state_cl_07'),
    ('l10n_cl_counties.state_cl_073', 'base.state_cl_07'),
    ('l10n_cl_counties.state_cl_074', 'base.state_cl_07'),
    ('l10n_cl_counties.state_cl_081', 'base.state_cl_08'),
    ('l10n_cl_counties.state_cl_082', 'base.state_cl_08'),
    ('l10n_cl_counties.state_cl_083', 'base.state_cl_08'),
    ('l10n_cl_counties.state_cl_091', 'base.state_cl_09'),
    ('l10n_cl_counties.state_cl_092', 'base.state_cl_09'),
    ('l10n_cl_counties.state_cl_101', 'base.state_cl_10'),
    ('l10n_cl_counties.state_cl_102', 'base.state_cl_10'),
    ('l10n_cl_counties.state_cl_103', 'base.state_cl_10'),
    ('l10n_cl_counties.state_cl_104', 'base.state_cl_10'),
    ('l10n_cl_counties.state_cl_111', 'base.state_cl_11'),
    ('l10n_cl_counties.state_cl_112', 'base.state_cl_11'),
    ('l10n_cl_counties.state_cl_113', 'base.state_cl_11'),
    ('l10n_cl_counties.state_cl_114', 'base.state_cl_11'),
    ('l10n_cl_counties.state_cl_121', 'base.state_cl_12'),
    ('l10n_cl_counties.state_cl_122', 'base.state_cl_12'),
    ('l10n_cl_counties.state_cl_123', 'base.state_cl_12'),
    ('l10n_cl_counties.state_cl_124', 'base.state_cl_12'),
    ('l10n_cl_counties.state_cl_131', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_132', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_133', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_134', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_135', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_136', 'base.state_cl_13'),
    ('l10n_cl_counties.state_cl_141', 'base.state_cl_14'),
    ('l10n_cl_counties.state_cl_142', 'base.state_cl_14'),
    ('l10n_cl_counties.state_cl_151', 'base.state_cl_15'),
    ('l10n_cl_counties.state_cl_152', 'base.state_cl_15'),

]


def migrate(cr, version):
    ENV = util.env(cr)
    new_states = {}
    for country_state in RES_COUNTRY_STATES:
        country_base_id = ENV.ref(country_state[1]).id
        if country_base_id not in new_states:
            new_states[country_base_id] = []
        new_states[country_base_id].append(ENV.ref(country_state[0]).id)
    for base_id, old_state_ids in new_states.items():
        cr.execute("UPDATE res_partner SET state_id={} WHERE state_id in {}".format(base_id, tuple(old_state_ids)))
    util.remove_view(cr, 'l10n_cl_counties.view_partner_form_states_city_inherit')
    util.remove_view(cr, 'l10n_cl_counties.view_move_form')
