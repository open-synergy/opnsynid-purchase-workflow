# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase


class TestPreparePurchaseOrderLine(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestPreparePurchaseOrderLine, self).setUp(*args, **kwargs)
        # Objects
        self.obj_purchase_requisition = self.env['purchase.requisition']
        self.obj_purchase_order = self.env['purchase.order']

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
                        'product_uom_id': self.uom.id,
                        'term_ids': [
                            (0, 0, data_purchase_term)
                        ]}),
                (0, 0, {'product_id': self.prod_2.id,
                        'product_qty': 5.0,
                        'product_uom_id': self.uom.id,
                        'term_ids': [
                            (0, 0, data_purchase_term)
                        ]}),
            ],
        }
        return data

    def test_prepare_purchase_order_line(self):
        # Create Purchase Requisition
        data_purchase_requisition = self._prepare_purchase_requisition()
        purchase_requisition = self.obj_purchase_requisition.\
            create(data_purchase_requisition)

        # Check Create Purchase Requisition
        self.assertIsNotNone(purchase_requisition)

        # Check Prepare Purchase Order Line
        data_prepare_po = self.obj_purchase_requisition.\
            _prepare_purchase_order(purchase_requisition, self.supplier)

        purchase_id = self.obj_purchase_order.create(data_prepare_po)

        for line in purchase_requisition.line_ids:
            x = []
            data_prepare_po_line = self.obj_purchase_requisition.\
                _prepare_purchase_order_line(
                    purchase_requisition, line, purchase_id.id, self.supplier)

            for term in line.term_ids:
                x.append(term.id)

            self.assertEqual(data_prepare_po_line.get('term_ids'), [(6, 0, x)])
