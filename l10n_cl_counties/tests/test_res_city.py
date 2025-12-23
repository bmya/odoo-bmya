from odoo.tests.common import TransactionCase


class TestChileanCities(TransactionCase):
    """Tests for Chilean cities/counties data"""

    def setUp(self):
        super().setUp()
        self.chile = self.env.ref('base.cl')

    def test_chilean_cities_loaded(self):
        """Test that Chilean cities are loaded from CSV"""
        cities = self.env['res.city'].search([
            ('country_id', '=', self.chile.id)
        ])

        self.assertGreater(
            len(cities),
            300,
            "Should have at least 300 Chilean cities/counties loaded"
        )

    def test_santiago_commune_exists(self):
        """Test that Santiago commune exists"""
        santiago = self.env['res.city'].search([
            ('name', '=', 'Santiago'),
            ('country_id', '=', self.chile.id),
        ], limit=1)

        self.assertTrue(
            santiago,
            "Santiago commune should exist in database"
        )
        self.assertEqual(
            santiago.state_id,
            self.env.ref('base.state_cl_13'),
            "Santiago should be in Región Metropolitana"
        )

    def test_all_cities_have_state(self):
        """Test that all Chilean cities have a state assigned"""
        cities_without_state = self.env['res.city'].search([
            ('country_id', '=', self.chile.id),
            ('state_id', '=', False),
        ])

        self.assertEqual(
            len(cities_without_state),
            0,
            "All Chilean cities should have a state assigned"
        )

    def test_key_communes_exist(self):
        """Test that key Chilean communes exist"""
        key_communes = [
            'Valparaíso',
            'Concepción',
            'La Serena',
            'Antofagasta',
            'Temuco',
            'Puerto Montt',
            'Punta Arenas',
        ]

        for commune_name in key_communes:
            commune = self.env['res.city'].search([
                ('name', '=', commune_name),
                ('country_id', '=', self.chile.id),
            ], limit=1)

            self.assertTrue(
                commune,
                f"Key commune {commune_name} should exist"
            )

    def test_no_duplicate_cities_per_state(self):
        """Test that there are no duplicate city names within the same state"""
        states = self.env['res.country.state'].search([
            ('country_id', '=', self.chile.id)
        ])

        for state in states:
            cities = self.env['res.city'].search([
                ('state_id', '=', state.id)
            ])

            city_names = cities.mapped('name')
            unique_names = set(city_names)

            self.assertEqual(
                len(city_names),
                len(unique_names),
                f"State {state.name} should not have duplicate city names"
            )
