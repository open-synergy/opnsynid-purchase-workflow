# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestDefaultDisplayName(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestDefaultDisplayName, self).setUp(*args, **kwargs)
        self.obj_purchase_term = self.env['purchase.term']

    def _prepare_data(self):
        data = {
            'name': 'Test Display 1',
            'code': 'DN-01',
            'active': True
            }
        return data

    def test_display_name(self):
        data = self._prepare_data()
        purchase_term = self.obj_purchase_term.create(data)

        # Check Create Purchase Term
        self.assertIsNotNone(purchase_term)

        # Check Display Name
        self.assertEqual(purchase_term.display_name, purchase_term.code)
