# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from datetime import datetime


class TestComputeOrderPolicy(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestComputeOrderPolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_purchase_order = self.env['purchase.order']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.partner = self.env.ref('base.res_partner_3')
        self.location = self.env.ref('stock.stock_location_stock')
        self.pricelist = self.env.ref('purchase.list0')
        self.product_1 =\
            self.env.ref('product.product_product_13')
        self.product_2 =\
            self.env.ref('product.product_product_25')
        self.uom = self.env.ref('product.product_uom_unit')
        self.po_type_reqular =\
            self.env.ref("purchase_order_type.po_type_regular")
        self.group_employee_id = self.ref('base.group_user')
        self.grp_po_manager =\
            self.env.ref(
                'purchase.group_purchase_manager')
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Button Bid Received
        self.grp_bid = self.obj_res_groups.create({
            'name': 'Regular - Group Button Bid Received'
        })
        # Add Group Button Send RFQ by Email
        self.grp_send_emailrfq = self.obj_res_groups.create({
            'name': 'Regular - Group Button Send RFQ by Email'
        })
        # Add Group Button Re-Send RFQ by Email
        self.grp_resend_emailrfq = self.obj_res_groups.create({
            'name': 'Regular - Group Button Re-Send RFQ by Email'
        })
        # Add Group Button Confirm Order
        self.grp_confirm_order = self.obj_res_groups.create({
            'name': 'Regular - Group Button Confirm Order'
        })
        # Add Group Button Manually Corrected (Shipping Exception)
        self.grp_manually_picking = self.obj_res_groups.create({
            'name': 'Regular - Group Button '
                    'Manually Corrected (Shipping Exception)'
        })
        # Add Group Button Manually Corrected (Invoice Exception)
        self.grp_manually_invoice = self.obj_res_groups.create({
            'name': 'Regular - Group Button '
                    'Manually Corrected (Invoice Exception)'
        })
        # Add Group Button Approve Order
        self.grp_approve_order = self.obj_res_groups.create({
            'name': 'Regular - Group Button Approve Order'
        })
        # Add Group Button Send PO by Email
        self.grp_send_emailpo = self.obj_res_groups.create({
            'name': 'Regular - Group Button Send PO by Email'
        })
        # Add Group Button Receive Products
        self.grp_receive_prod = self.obj_res_groups.create({
            'name': 'Regular - Group Button Receive Products'
        })
        # Add Group Button Receive Invoice
        self.grp_receive_inv = self.obj_res_groups.create({
            'name': 'Regular - Group Button Receive Invoice'
        })
        # Add Group Button Set To Draft
        self.grp_settodraft_order = self.obj_res_groups.create({
            'name': 'Regular - Group Button Set To Draft'
        })
        # Add Group Button Cancel
        self.grp_cancel_order = self.obj_res_groups.create({
            'name': 'Regular - Group Button Cancel'
        })

    def _create_user_1(self):
        val = {
            'name': 'User Test 1',
            'login': 'user_1',
            'alias_name': 'user1',
            'email': 'user_test_1@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_1 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_1

    def _create_user_2(self):
        val = {
            'name': 'User Test 2',
            'login': 'user_2',
            'alias_name': 'user2',
            'email': 'user_test_2@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_2 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_2

    def _create_user_3(self):
        val = {
            'name': 'User Test 3',
            'login': 'user_3',
            'alias_name': 'user3',
            'email': 'user_test_3@example.com',
            'notify_email': 'none',
            'groups_id': [(
                6, 0, [
                    self.group_employee_id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_3 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_3

    def _create_purchase_order(self, order_type_id):
        if order_type_id:
            type_id = order_type_id.id
        else:
            type_id = False

        # Create Purchase Order
        purchase_order = self.obj_purchase_order.create({
            'partner_id': self.partner.id,
            'location_id': self.location.id,
            'pricelist_id': self.pricelist.id,
            'order_type': type_id,
            'order_line': [
                (0, 0, {'product_id': self.product_1.id,
                        'name': self.product_1.name,
                        'price_unit': self.product_1.standard_price,
                        'date_planned': datetime.now().strftime("%Y-%m-%d"),
                        'product_qty': 42.0}),
                (0, 0, {'product_id': self.product_2.id,
                        'name': self.product_2.name,
                        'price_unit': self.product_2.standard_price,
                        'date_planned': datetime.now().strftime("%Y-%m-%d"),
                        'product_qty': 12.0})
            ]
        })

        return purchase_order

    def test_compute_case_admin(self):
        # Create Purchase Order
        purchase_order =\
            self._create_purchase_order(False)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, purchase_order.bid_ok)
        self.assertEqual(True, purchase_order.send_emailrfq_ok)
        self.assertEqual(True, purchase_order.resend_emailrfq_ok)
        self.assertEqual(True, purchase_order.confirm_order_ok)
        self.assertEqual(True, purchase_order.manually_picking_ok)
        self.assertEqual(True, purchase_order.manually_invoice_ok)
        self.assertEqual(True, purchase_order.approve_order_ok)
        self.assertEqual(True, purchase_order.send_emailpo_ok)
        self.assertEqual(True, purchase_order.receive_prod_ok)
        self.assertEqual(True, purchase_order.receive_inv_ok)
        self.assertEqual(True, purchase_order.settodraft_order_ok)
        self.assertEqual(True, purchase_order.cancel_order_ok)

    def test_compute_case_no_type(self):
        # Create Purchase Order
        purchase_order =\
            self._create_purchase_order(False)

        # Condition :
        #   1. No Purchase Order Type
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).cancel_order_ok
        )

    def test_compute_case_1(self):
        # Create Purchase Order
        purchase_order =\
            self._create_purchase_order(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Bid Received has group
        #   3. Allowed to Send RFQ by Email has group
        #   4. Allowed to Re-Send RFQ by Email has group
        #   5. Allowed to Confirm Order has group
        #   6. User 1 doesn't have group
        self.po_type_reqular.bid_group_ids = [(
            6, 0, [
                self.grp_bid.id
            ]
        )]

        self.po_type_reqular.send_emailrfq_group_ids = [(
            6, 0, [
                self.grp_send_emailrfq.id
            ]
        )]

        self.po_type_reqular.resend_emailrfq_group_ids = [(
            6, 0, [
                self.grp_resend_emailrfq.id
            ]
        )]

        self.po_type_reqular.confirm_order_group_ids = [(
            6, 0, [
                self.grp_confirm_order.id
            ]
        )]
        # Result
        #   1. User 1 cannot Bid Received
        #   2. User 1 cannot Send RFQ by Email
        #   3. User 1 cannot Re-Send RFQ by Email
        #   4. User 1 cannot Confirm Order

        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_1.id).bid_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_1.id).send_emailrfq_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_1.id).resend_emailrfq_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).cancel_order_ok
        )

        # Condition :
        #   1. User 1 have group
        # Add Group Bid Received
        self.user_1.groups_id = [(
            4,
            self.grp_bid.id
        )]
        # Add Group Send RFQ by Email
        self.user_1.groups_id = [(
            4,
            self.grp_send_emailrfq.id
        )]
        # Add Group Re-Send RFQ by Email
        self.user_1.groups_id = [(
            4,
            self.grp_resend_emailrfq.id
        )]
        # Add Group Confirm Order
        self.user_1.groups_id = [(
            4,
            self.grp_confirm_order.id
        )]

        # Result
        #   1. User 1 can Bid Received
        #   2. User 1 can Send RFQ by Email
        #   3. User 1 can Re-Send RFQ by Email
        #   4. User 1 can Confirm Order
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_1.id).cancel_order_ok
        )

    def test_compute_case_2(self):
        # Create Purchase Order
        purchase_order =\
            self._create_purchase_order(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 2
        #   2. Allowed to Manually Corrected (Shipping Exception) has group
        #   3. Allowed to Manually Corrected (Invoice Exception) has group
        #   4. Allowed to Approve Order has group
        #   5. Allowed to Send PO by Email has group
        #   6. User 2 doesn't have group
        self.po_type_reqular.manually_picking_group_ids = [(
            6, 0, [
                self.grp_manually_picking.id
            ]
        )]

        self.po_type_reqular.manually_invoice_group_ids = [(
            6, 0, [
                self.grp_manually_invoice.id
            ]
        )]

        self.po_type_reqular.approve_order_group_ids = [(
            6, 0, [
                self.grp_approve_order.id
            ]
        )]

        self.po_type_reqular.send_emailpo_group_ids = [(
            6, 0, [
                self.grp_send_emailpo.id
            ]
        )]
        # Result
        #   1. User 2 cannot Manually Corrected (Shipping Exception)
        #   2. User 2 cannot Manually Corrected (Invoice Exception)
        #   3. User 2 cannot Approve Order
        #   4. User 2 cannot Send PO by Email

        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).confirm_order_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_2.id).manually_picking_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_2.id).manually_invoice_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_2.id).approve_order_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_2.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).cancel_order_ok
        )

        # Condition :
        #   1. User 2 have group
        # Add Group Manually Corrected (Shipping Exception)
        self.user_2.groups_id = [(
            4,
            self.grp_manually_picking.id
        )]
        # Add Group Manually Corrected (Invoice Exception)
        self.user_2.groups_id = [(
            4,
            self.grp_manually_invoice.id
        )]
        # Add Group Approve Order
        self.user_2.groups_id = [(
            4,
            self.grp_approve_order.id
        )]
        # Add Group Send PO by Email
        self.user_2.groups_id = [(
            4,
            self.grp_send_emailpo.id
        )]

        # Result
        #   1. User 2 can Manually Corrected (Shipping Exception)
        #   2. User 2 can Manually Corrected (Invoice Exception)
        #   3. User 2 can Approve Order
        #   4. User 2 can Send PO by Email
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_2.id).cancel_order_ok
        )

    def test_compute_case_3(self):
        # Create Purchase Order
        purchase_order =\
            self._create_purchase_order(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 3
        #   2. Allowed to Receive Products has group
        #   3. Allowed to Receive Invoice has group
        #   4. Allowed to Set To Draft has group
        #   5. Allowed to Cancel has group
        #   6. User 3 doesn't have group
        self.po_type_reqular.receive_prod_group_ids = [(
            6, 0, [
                self.grp_receive_prod.id
            ]
        )]

        self.po_type_reqular.receive_inv_group_ids = [(
            6, 0, [
                self.grp_receive_inv.id
            ]
        )]

        self.po_type_reqular.settodraft_order_group_ids = [(
            6, 0, [
                self.grp_settodraft_order.id
            ]
        )]

        self.po_type_reqular.cancel_order_group_ids = [(
            6, 0, [
                self.grp_cancel_order.id
            ]
        )]
        # Result
        #   1. User 3 cannot Receive Products
        #   2. User 3 cannot Receive Invoice
        #   3. User 3 cannot Set To Draft
        #   4. User 3 cannot Cancel

        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).send_emailpo_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_3.id).receive_prod_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_3.id).receive_inv_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_3.id).settodraft_order_ok
        )
        self.assertEqual(
            False,
            purchase_order.sudo(
                self.user_3.id).cancel_order_ok
        )

        # Condition :
        #   1. User 3 have group
        # Add Group Receive Products
        self.user_3.groups_id = [(
            4,
            self.grp_receive_prod.id
        )]
        # Add Group Receive Invoice
        self.user_3.groups_id = [(
            4,
            self.grp_receive_inv.id
        )]
        # Add Group Set To Draft
        self.user_3.groups_id = [(
            4,
            self.grp_settodraft_order.id
        )]
        # Add Group Cancel
        self.user_3.groups_id = [(
            4,
            self.grp_cancel_order.id
        )]

        # Result
        #   1. User 3 can Receive Products
        #   2. User 3 can Receive Invoice
        #   3. User 3 can Set To Draft
        #   4. User 3 can Cancel
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).bid_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).send_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).resend_emailrfq_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).confirm_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).manually_picking_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).manually_invoice_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).approve_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).send_emailpo_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).receive_prod_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).receive_inv_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).settodraft_order_ok
        )
        self.assertEqual(
            True,
            purchase_order.sudo(
                self.user_3.id).cancel_order_ok
        )
