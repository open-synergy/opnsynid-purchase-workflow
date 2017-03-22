# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputePolicy(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputePolicy, self).setUp(*args, **kwargs)
        # Objects
        self.obj_purchase_req = self.env['purchase.request']
        self.obj_purchase_req_line =\
            self.env['purchase.request.line']
        self.obj_res_groups = self.env['res.groups']
        self.obj_res_users = self.env['res.users']

        # Data
        self.group_employee_id = self.ref('base.group_user')
        self.grp_public = self.env.ref('base.group_public')
        self.product = self.env.ref('product.product_product_13')
        self.uom = self.env.ref('product.product_uom_unit')
        self.po_type_reqular =\
            self.env.ref("purchase_order_type.po_type_regular")
        self.grp_pr_manager =\
            self.env.ref(
                'purchase_request.group_purchase_request_manager')
        self.grp_po_manager =\
            self.env.ref(
                'purchase.group_purchase_manager')
        self.user_1 = self._create_user_1()
        self.user_2 = self._create_user_2()
        self.user_3 = self._create_user_3()

        # Add Group Button Request
        self.grp_request = self.obj_res_groups.create({
            'name': 'Regular - Group Button Request'
        })
        # Add Group Button Approve
        self.grp_approve = self.obj_res_groups.create({
            'name': 'Regular - Group Button Approve'
        })
        # Add Group Button Reject
        self.grp_reject = self.obj_res_groups.create({
            'name': 'Regular - Group Button Reject'
        })
        # Add Group Button Reset
        self.grp_reset = self.obj_res_groups.create({
            'name': 'Regular - Group Button Reset'
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
                    self.grp_pr_manager.id,
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
                    self.grp_pr_manager.id,
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
                    self.grp_pr_manager.id,
                    self.grp_po_manager.id
                ]
            )]
        }
        user_3 = self.obj_res_users.with_context({
            'no_reset_password': True
        }).create(val)
        return user_3

    def _create_purchase_request(self, order_type_id):
        if order_type_id:
            type_id = order_type_id.id
        else:
            type_id = False

        # Create Purchase Request
        purchase_req = self.obj_purchase_req.create({
            'order_type_id': type_id
        })

        # Create Purchase Request Line
        vals = {
            'request_id': purchase_req.id,
            'product_id': self.product.id,
            'product_uom_id': self.uom.id,
            'product_qty': 5.0,
        }
        self.obj_purchase_req_line.create(vals)

        return purchase_req

    def test_compute_case_admin(self):
        # Create Purchase Request
        purchase_request =\
            self._create_purchase_request(False)

        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, purchase_request.request_ok)
        self.assertEqual(True, purchase_request.approve_ok)
        self.assertEqual(True, purchase_request.reject_ok)
        self.assertEqual(True, purchase_request.reset_ok)

    def test_compute_case_no_type(self):
        # Create Purchase Request
        purchase_request =\
            self._create_purchase_request(False)

        # Condition :
        #   1. No Purchase Request Type
        self.assertEqual(True, purchase_request.request_ok)
        self.assertEqual(True, purchase_request.approve_ok)
        self.assertEqual(True, purchase_request.reject_ok)
        self.assertEqual(True, purchase_request.reset_ok)

    def test_compute_case_1(self):
        # Create Purchase Request
        purchase_request =\
            self._create_purchase_request(self.po_type_reqular)

        # Condition :
        #   1. Log In As User 1
        #   2. Allowed to Request Approval has group
        #   3. Allowed to Approve has group
        #   4. Allowed to Reject doesn't have group
        #   5. Allowed to Reset doesn't have group
        #   6. User 1 doesn't have group
        self.po_type_reqular.request_group_ids = [(
            6, 0, [
                self.grp_request.id
            ]
        )]

        self.po_type_reqular.approve_group_ids = [(
            6, 0, [
                self.grp_approve.id
            ]
        )]

        # Result
        #   1. User 1 cannot Request Approval
        #   2. User 1 User cannot Approve
        #   3. User 1 User can Reject
        #   4. User 1 User can Reset

        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_1.id).request_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_1.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).reset_ok
        )

        # Condition :
        #   1. User 1 have group
        # Add Group Request
        self.user_1.groups_id = [(
            4,
            self.grp_request.id
        )]
        # Add Group Approve
        self.user_1.groups_id = [(
            4,
            self.grp_approve.id
        )]

        # Result
        #   1. User 1 can Request Approval
        #   2. User 1 can Approve
        #   3. User 1 can Reject
        #   4. User 1 can Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_1.id).reset_ok
        )

    def test_compute_case_2(self):
        # Create Purchase Request
        purchase_request =\
            self._create_purchase_request(self.po_type_reqular)

        # Condition :
        #   1. Log In as User 2
        #   2. Allowed to Request Approval doesn't have group
        #   3. Allowed to Approve doesn't have group
        #   4. Allowed to Reject has group
        #   5. Allowed to Reset has group
        #   6. Public User doesn't have group
        self.po_type_reqular.reject_group_ids = [(
            6, 0, [
                self.grp_reject.id
            ]
        )]

        self.po_type_reqular.reset_group_ids = [(
            6, 0, [
                self.grp_reset.id
            ]
        )]

        # Result
        #   1. User 2 can Request Approval
        #   2. User 2 can Approve
        #   3. User 2 cannot Reject
        #   4. User 2 cannot Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).approve_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_2.id).reject_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_2.id).reset_ok
        )

        # Condition :
        #   1. User 2 have group
        # Add Group Reject
        self.user_2.groups_id = [(
            4,
            self.grp_reject.id,
        )]
        # Add Group Reset
        self.user_2.groups_id = [(
            4,
            self.grp_reset.id
        )]

        # Result
        #   1. User 2 can Request Approval
        #   2. User 2 User can Approve
        #   3. User 2 User can Reject
        #   4. User 2 User can Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_2.id).reset_ok
        )

    def test_compute_case_3(self):
        # Create Purchase Request
        purchase_request =\
            self._create_purchase_request(self.po_type_reqular)

        # Condition :
        #   1. Log In as User 3
        self.po_type_reqular.request_group_ids = [(
            6, 0, [
                self.grp_request.id
            ]
        )]

        self.po_type_reqular.approve_group_ids = [(
            6, 0, [
                self.grp_approve.id
            ]
        )]
        self.po_type_reqular.reject_group_ids = [(
            6, 0, [
                self.grp_reject.id
            ]
        )]

        self.po_type_reqular.reset_group_ids = [(
            6, 0, [
                self.grp_reset.id
            ]
        )]

        # Result
        #   1. User 3 cannot Request Approval
        #   2. User 3 cannot Approve
        #   3. User 3 cannot Reject
        #   4. User 3 cannot Reset
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_3.id).request_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_3.id).approve_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_3.id).reject_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.user_3.id).reset_ok
        )

        # Condition :
        #   1. User 3 have group
        # Add Group Reject
        self.user_3.groups_id = [(
            4,
            self.grp_request.id
        )]
        # Add Group Approve
        self.user_3.groups_id = [(
            4,
            self.grp_approve.id
        )]
        self.user_3.groups_id = [(
            4,
            self.grp_reject.id,
        )]
        # Add Group Reset
        self.user_3.groups_id = [(
            4,
            self.grp_reset.id
        )]

        # Result
        #   1. User 3 can Request Approval
        #   2. User 3 User can Approve
        #   3. User 3 User can Reject
        #   4. User 3 User can Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_3.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_3.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_3.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.user_3.id).reset_ok
        )
