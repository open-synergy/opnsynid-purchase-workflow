# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputeRequisitionPolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputeRequisitionPolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_purchase_requisition = self.env['purchase.requisition']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.product_1 =\
            self.env.ref('product.product_product_8')
        self.product_2 =\
            self.env.ref('product.product_product_9')
        self.uom = self.env.ref('product.product_uom_unit')
        self.po_type_reqular =\
            self.env.ref("purchase_order_type.po_type_regular")
        self.group_employee_id = self.ref('base.group_user')
        self.grp_pr_manager =\
            self.env.ref(
                'purchase_requisition.group_purchase_requisition_manager')
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Button Confirm Call
        self.grp_sent_supplier = self.obj_res_groups.create({
            'name': 'Regular - Group Button Confirm Call'
        })
        # Add Group Button Close Call for Bids
        self.grp_open_bid = self.obj_res_groups.create({
            'name': 'Regular - Group Button Close Call for Bids'
        })
        # Add Group Button Reset to Draft
        self.grp_tender_reset = self.obj_res_groups.create({
            'name': 'Regular - Group Button Reset to Draft'
        })
        # Add Group Button Choose product lines
        self.grp_open_product = self.obj_res_groups.create({
            'name': 'Regular - Group Button Choose product lines'
        })
        # Add Group Button Done
        self.grp_generate_po = self.obj_res_groups.create({
            'name': 'Regular - Group Button Done'
        })
        # Add Group Button Cancel Call
        self.grp_cancel_requisition = self.obj_res_groups.create({
            'name': 'Regular - Group Button Cancel Call'
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
                    self.grp_pr_manager.id
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
                    self.grp_pr_manager.id
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
                    self.grp_pr_manager.id
                ]
            )]
        }
        user_3 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_3

    def _create_purchase_requisition(self, order_type_id):
        if order_type_id:
            type_id = order_type_id.id
        else:
            type_id = False

        # Create Purchase Requisition
        purchase_requisition = self.obj_purchase_requisition.create({
            'exclusive': 'exclusive',
            'order_type': type_id,
            'line_ids': [
                (0, 0, {'product_id': self.product_1.id,
                        'product_qty': 5.0,
                        'product_uom_id': self.uom.id}),
                (0, 0, {'product_id': self.product_2.id,
                        'product_qty': 5.0,
                        'product_uom_id': self.uom.id})
            ],
        })

        return purchase_requisition

    def test_compute_case_admin(self):
        # Create Purchase Requisition
        purchase_requisition =\
            self._create_purchase_requisition(False)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, purchase_requisition.sent_supplier_ok)
        self.assertEqual(True, purchase_requisition.open_bid_ok)
        self.assertEqual(True, purchase_requisition.tender_reset_ok)
        self.assertEqual(True, purchase_requisition.open_product_ok)
        self.assertEqual(True, purchase_requisition.generate_po_ok)
        self.assertEqual(True, purchase_requisition.cancel_requisition_ok)

    def test_compute_case_no_type(self):
        # Create Purchase Requisition
        purchase_requisition =\
            self._create_purchase_requisition(False)

        # Condition :
        #   1. No Purchase Order Type
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).cancel_requisition_ok
        )

    def test_compute_case_1(self):
        # Create Purchase Requisition
        purchase_requisition =\
            self._create_purchase_requisition(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Confirm Call has group
        #   3. Allowed to Close Call for Bids has group
        #   4. User 1 doesn't have group
        self.po_type_reqular.sent_supplier_group_ids = [(
            6, 0, [
                self.grp_sent_supplier.id
            ]
        )]

        self.po_type_reqular.open_bid_group_ids = [(
            6, 0, [
                self.grp_open_bid.id
            ]
        )]
        # Result
        #   1. User 1 cannot Confirm Call has group
        #   2. User 1 cannot Close Call for Bids has group

        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_1.id).sent_supplier_ok
        )
        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_1.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).cancel_requisition_ok
        )

        # Condition :
        #   1. User 1 have group
        # Add Group Confirm Call
        self.user_1.groups_id = [(
            4,
            self.grp_sent_supplier.id
        )]
        # Add Group Close Call for Bids
        self.user_1.groups_id = [(
            4,
            self.grp_open_bid.id
        )]

        # Result
        #   1. User 1 can Confirm Call
        #   2. User 1 can Close Call for Bids
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_1.id).cancel_requisition_ok
        )

    def test_compute_case_2(self):
        # Create Purchase Requisition
        purchase_requisition =\
            self._create_purchase_requisition(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 2
        #   2. Allowed to Reset to Draft has group
        #   3. Allowed to Choose product lines has group
        #   4. User 2 doesn't have group
        self.po_type_reqular.tender_reset_group_ids = [(
            6, 0, [
                self.grp_tender_reset.id
            ]
        )]

        self.po_type_reqular.open_product_group_ids = [(
            6, 0, [
                self.grp_open_product.id
            ]
        )]
        # Result
        #   1. User 2 cannot Reset to Draft
        #   2. User 2 cannot Choose product lines

        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).open_bid_ok
        )
        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_2.id).tender_reset_ok
        )
        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_2.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).cancel_requisition_ok
        )

        # Condition :
        #   1. User 2 have group
        # Add Group Reset to Draft
        self.user_2.groups_id = [(
            4,
            self.grp_tender_reset.id
        )]
        # Add Group Choose product lines
        self.user_2.groups_id = [(
            4,
            self.grp_open_product.id
        )]

        # Result
        #   1. User 2 can Reset to Draft
        #   2. User 2 can Choose product lines
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_2.id).cancel_requisition_ok
        )

    def test_compute_case_3(self):
        # Create Purchase Requisition
        purchase_requisition =\
            self._create_purchase_requisition(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 3
        #   2. Allowed to Done has group
        #   3. Allowed to Cancel Call has group
        #   4. User 3 doesn't have group
        self.po_type_reqular.generate_po_group_ids = [(
            6, 0, [
                self.grp_generate_po.id
            ]
        )]

        self.po_type_reqular.cancel_requisition_group_ids = [(
            6, 0, [
                self.grp_cancel_requisition.id
            ]
        )]
        # Result
        #   1. User 3 cannot Done
        #   2. User 3 cannot Cancel Call

        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).open_product_ok
        )
        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_3.id).generate_po_ok
        )
        self.assertEqual(
            False,
            purchase_requisition.sudo(
                self.user_3.id).cancel_requisition_ok
        )

        # Condition :
        #   1. User 3 have group
        # Add Group Done
        self.user_3.groups_id = [(
            4,
            self.grp_generate_po.id
        )]
        # Add Group Cancel Call
        self.user_3.groups_id = [(
            4,
            self.grp_cancel_requisition.id
        )]

        # Result
        #   1. User 3 can Done
        #   2. User 3 can Cancel Call
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).sent_supplier_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).open_bid_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).tender_reset_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).open_product_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).generate_po_ok
        )
        self.assertEqual(
            True,
            purchase_requisition.sudo(
                self.user_3.id).cancel_requisition_ok
        )
