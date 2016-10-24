# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common


class TestDefaultOrderType(common.TransactionCase):

    def setUp(self):
        super(TestDefaultOrderType, self).setUp()
        self.purchase_request = self.env['purchase.request']
        self.purchase_order_type = self.env['purchase.order.type']

    def test_purchase_request_status(self):
        default_order_type = self.purchase_order_type.search(
            [], limit=1)

        defaults = self.purchase_request.default_get(
            ['order_type_id'])

        self.assertEqual(
            default_order_type.id, defaults.get('order_type_id'))
