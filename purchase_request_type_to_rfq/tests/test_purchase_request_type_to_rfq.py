# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from openerp.tools import SUPERUSER_ID
from openerp.exceptions import Warning as UserError
from lxml import etree


class TestPurchaseRequestTypeToRfq(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseRequestTypeToRfq, self).setUp()
        # Data Object
        self.purchase_request = self.env['purchase.request']
        self.purchase_request_line = self.env['purchase.request.line']
        self.wiz =\
            self.env['purchase.request.line.make.purchase.order']
        self.purchase_order = self.env['purchase.order']
        # Data Order Type
        self.order_type = self.env.ref('purchase_order_type.po_type_contract')
        self.order_type_2 = self.env.ref('purchase_order_type.po_type_planned')
        # Data Picking Type
        self.picking_type = self.env.ref('stock.picking_type_in')
        # Data Product & Uom
        self.product_1 = self.env.ref('product.product_product_13')
        self.product_2 = self.env.ref('product.product_product_14')
        self.uom = self.env.ref('product.product_uom_unit')
        # Data Supplier
        self.supplier = self.env.ref('base.res_partner_12')

    def _prepare_purchase_request(self):
        data = {
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'order_type_id': self.order_type.id,
            'requested_by': SUPERUSER_ID,
        }
        return data

    def _prepare_purchase_request_2(self):
        data = {
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'order_type_id': self.order_type_2.id,
            'requested_by': SUPERUSER_ID,
        }
        return data

    def _prepare_purchase_request_lines(self, pr_id):
        data = {
            'request_id': pr_id,
            'product_id': self.product_1.id,
            'product_uom_id': self.uom.id,
            'product_qty': 5.0,
        }
        return data

    def _prepare_purchase_request_lines_2(self, pr_id):
        data = {
            'request_id': pr_id,
            'product_id': self.product_2.id,
            'product_uom_id': self.uom.id,
            'product_qty': 7.0,
        }
        return data

    def check_fields_view_get(self, pr_line_id):
        view = self.wiz.with_context({
            'form_view_ref': 'purchase_request_type_to_rfq\
                .purchase_request_line_make_purchase_order_view_form'},
            active_ids=[pr_line_id],
            active_id=pr_line_id,
        ).fields_view_get()
        doc = etree.XML(view['arch'])
        for node in doc.xpath("//field[@name='purchase_order_id']"):
            domain = node.get('domain')
            self.assertEquals(
                domain,
                "[('order_type', 'in', [%s])]" % self.order_type.id
            )
        return True

    def test_get_order_type_error(self):
        # Create Purchase Request - 1
        data_pr = self._prepare_purchase_request()
        pr_1 = self.purchase_request.create(data_pr)

        # Create Purchase Request Lines - 1
        data_pr_lines = self._prepare_purchase_request_lines(pr_1.id)
        pr_line_1 = self.purchase_request_line.create(data_pr_lines)

        pr_1.button_to_approve()
        pr_1.button_approved()

        # Create Purchase Request - 2
        data_pr_2 = self._prepare_purchase_request_2()
        pr_2 = self.purchase_request.create(data_pr_2)

        # Create Purchase Request Lines - 2
        data_pr_lines_2 = self._prepare_purchase_request_lines_2(pr_2.id)
        pr_line_2 = self.purchase_request_line.create(data_pr_lines_2)

        pr_2.button_to_approve()
        pr_2.button_approved()

        # Create Wizard
        active_ids = [pr_line_1.id]
        active_ids.append(pr_line_2.id)

        vals = {
            'supplier_id': self.supplier.id,
        }
        wiz_id = self.wiz.with_context(
            active_model="purchase.request.line",
            active_ids=active_ids,).create(vals)

        # Create Purchase Order & Check Error
        with self.assertRaises(UserError):
            wiz_id.make_purchase_order()

    def test_purchase_request_order_type(self):
        # Create Purchase Request
        data_pr = self._prepare_purchase_request()
        pr = self.purchase_request.create(data_pr)

        # Create Purchase Request Lines
        data_pr_lines = self._prepare_purchase_request_lines(pr.id)
        pr_line = self.purchase_request_line.create(data_pr_lines)

        pr.button_to_approve()
        pr.button_approved()

        # Check fields_view_get
        self.check_fields_view_get(pr_line.id)

        # Create Wizard
        vals = {
            'supplier_id': self.supplier.id,
        }
        wiz_id = self.wiz.with_context(
            active_model="purchase.request.line",
            active_ids=[pr_line.id],
            active_id=pr_line.id,).create(vals)

        # Create Purchase Order
        wiz_id.make_purchase_order()

        # Check Order Type
        order_id = pr_line.purchase_lines.order_id
        domain = [
            ('id', '=', order_id.id),
        ]
        purchase = self.purchase_order.search(domain)

        order_type_id = wiz_id._get_order_type()

        self.assertEquals(
            order_type_id,
            purchase.order_type.id
        )
