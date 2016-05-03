# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestPreparePurchaseOrder(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestPreparePurchaseOrder, self).setUp(*args, **kwargs)
        # Objects
        self.obj_purchase_requisition = self.env['purchase.requisition']

        # Data Products
        self.prod_1 = self.env.ref('product.product_product_8')
        self.prod_2 = self.env.ref('product.product_product_9')
        self.uom = self.env.ref('product.product_uom_unit')

        # Data Supplier
        self.supplier = self.env.ref('base.res_partner_2')

    def _prepare_purchase_term(self):
        data = {
            'name': 'Test Display 1',
            'code': 'DN-01',
            'active': True
            }
        return data

    def _prepare_purchase_requisition(self):
        data_purchase_term = self._prepare_purchase_term()
        data = {
            'exclusive': 'exclusive',
            'line_ids': [
                (0, 0, {'product_id': self.prod_1.id,
                        'product_qty': 5.0,
                        'product_uom_id': self.uom.id}),
                (0, 0, {'product_id': self.prod_2.id,
                        'product_qty': 5.0,
                        'product_uom_id': self.uom.id})
            ],
            'term_ids': [
                (0, 0, data_purchase_term)
            ]
        }
        return data

    def test_prepare_purchase_order(self):
        x = []
        #Create Purchase Requisition
        data_purchase_requisition = self._prepare_purchase_requisition()
        purchase_requisition = self.obj_purchase_requisition.\
            create(data_purchase_requisition)

        # Check Create Purchase Requisition
        self.assertIsNotNone(purchase_requisition)

        # Get Purchase Term
        for term in purchase_requisition.term_ids:
            x.append(term.id)

        # Check Purchase Term
        self.assertIsNotNone(x)

        # Check Prepare Purchase Order
        data_prepare_po = self.obj_purchase_requisition.\
            _prepare_purchase_order(purchase_requisition, self.supplier)

        self.assertEqual(data_prepare_po.get('term_ids'), [(6, 0, x)])
