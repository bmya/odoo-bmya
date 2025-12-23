from odoo.tests.common import TransactionCase


class TestResPartnerCounties(TransactionCase):
    """Tests for Chilean counties integration in res.partner"""

    def setUp(self):
        super().setUp()
        # Set up Chilean company
        self.company_cl = self.env.user.company_id
        self.company_cl.country_id = self.env.ref('base.cl')

        # Get Chilean regions and cities
        self.region_metropolitana = self.env.ref('base.state_cl_13')  # RM
        self.region_valparaiso = self.env.ref('base.state_cl_05')     # V

        # Find Chilean cities/counties
        self.santiago = self.env['res.city'].search([
            ('name', '=', 'Santiago'),
            ('state_id', '=', self.region_metropolitana.id)
        ], limit=1)

        self.valparaiso = self.env['res.city'].search([
            ('name', '=', 'Valparaíso'),
            ('state_id', '=', self.region_valparaiso.id)
        ], limit=1)

    def test_partner_default_country_chile(self):
        """Test that new partners get Chile as default country"""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner CL',
        })
        self.assertEqual(
            partner.country_id,
            self.env.ref('base.cl'),
            "Default country should be Chile"
        )

    def test_city_updates_state_and_city_name(self):
        """Test that selecting city_id updates state_id and city name"""
        partner = self.env['res.partner'].create({
            'name': 'Test Partner Santiago',
            'country_id': self.env.ref('base.cl').id,
            'city_id': self.santiago.id,
        })

        self.assertEqual(
            partner.state_id,
            self.region_metropolitana,
            "State should be automatically set from city_id"
        )
        self.assertEqual(
            partner.city,
            'Santiago',
            "City name should match city_id name"
        )

    def test_real_city_for_santiago(self):
        """Test that Santiago region shows 'Santiago' as real_city"""
        partner = self.env['res.partner'].create({
            'name': 'Test Santiago',
            'country_id': self.env.ref('base.cl').id,
            'city_id': self.santiago.id,
        })

        self.assertEqual(
            partner.real_city,
            'Santiago',
            "Real city for Santiago region should be 'Santiago'"
        )

    def test_real_city_for_other_regions(self):
        """Test that other regions use city_id.name as real_city"""
        if not self.valparaiso:
            self.skipTest("Valparaíso city not found in database")

        partner = self.env['res.partner'].create({
            'name': 'Test Valparaíso',
            'country_id': self.env.ref('base.cl').id,
            'city_id': self.valparaiso.id,
        })

        self.assertEqual(
            partner.real_city,
            self.valparaiso.name,
            "Real city should match city_id name for non-Santiago regions"
        )

    def test_non_chile_partner_no_automatic_state(self):
        """Test that non-Chilean partners don't get automatic state/city updates"""
        partner = self.env['res.partner'].create({
            'name': 'Test Foreign',
            'country_id': self.env.ref('base.us').id,
        })

        self.assertFalse(
            partner.real_city,
            "Non-Chilean partner should not have real_city set"
        )

    def test_company_country_code_cl(self):
        """Test company_country_code is 'CL' for Chilean partners"""
        partner = self.env['res.partner'].create({
            'name': 'Test CL Code',
            'country_id': self.env.ref('base.cl').id,
            'company_id': self.company_cl.id,
        })

        self.assertEqual(
            partner.company_country_code,
            'CL',
            "Company country code should be 'CL' for Chilean partners"
        )
