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
        self.public_user = self.env.ref('base.public_user')
        # Add Group Purchase Request Manager
        self.public_user.groups_id = [(
            4,
            self.grp_pr_manager.id
        )]
        # Add Group Purchase Manager
        self.public_user.groups_id = [(
            4,
            self.grp_po_manager.id
        )]

    def _create_purchase_request(self, order_type_id):
        # Create Purchase Request
        purchase_req = self.obj_purchase_req.create({
            'order_type_id': order_type_id.id
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

    def test_compute_case_1(self):
        purchase_request =\
            self._create_purchase_request(self.po_type_reqular)

        grp_request = self.obj_res_groups.create({
            'name': 'Regular - Group Button Request'
        })

        grp_approve = self.obj_res_groups.create({
            'name': 'Regular - Group Button Approve'
        })

        grp_reject = self.obj_res_groups.create({
            'name': 'Regular - Group Button Reject'
        })

        grp_reset = self.obj_res_groups.create({
            'name': 'Regular - Group Button Reset'
        })
        # Condition :
        #   1. Test for User Admin
        self.assertEqual(True, purchase_request.request_ok)
        self.assertEqual(True, purchase_request.approve_ok)
        self.assertEqual(True, purchase_request.reject_ok)
        self.assertEqual(True, purchase_request.reset_ok)

        # Condition :
        #   1. Allowed to Request Approval has group
        #   2. Allowed to Approve has group
        #   3. Public User doesn't have group
        self.po_type_reqular.request_group_ids = [(
            6, 0, [
                grp_request.id
            ]
        )]

        self.po_type_reqular.approve_group_ids = [(
            6, 0, [
                grp_approve.id
            ]
        )]

        # Result
        #   1. Public User cannot Request Approval
        #   2. Public User cannot Approve
        #   3. Public User can Reject
        #   4. Public User can Reset

        self.assertEqual(
            False,
            purchase_request.sudo(
                self.public_user.id).request_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.public_user.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reset_ok
        )

        # Condition :
        #   1. Public User have group
        # Add Group Request
        self.public_user.groups_id = [(
            4,
            grp_request.id
        )]
        # Add Group Approve
        self.public_user.groups_id = [(
            4,
            grp_approve.id
        )]

        # Result
        #   1. Public User can Request Approval
        #   2. Public User can Approve
        #   3. Public User can Reject
        #   4. Public User can Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reset_ok
        )

        # Condition :
        #   1. Allowed to Reject has group
        #   2. Allowed to Reset has group
        #   3. Public User doesn't have group
        self.po_type_reqular.reject_group_ids = [(
            6, 0, [
                grp_reject.id
            ]
        )]

        self.po_type_reqular.reset_group_ids = [(
            6, 0, [
                grp_reset.id
            ]
        )]

        # Result
        #   1. Public User can Request Approval
        #   2. Public User can Approve
        #   3. Public User cannot Reject
        #   4. Public User cannot Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).approve_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.public_user.id).reject_ok
        )
        self.assertEqual(
            False,
            purchase_request.sudo(
                self.public_user.id).reset_ok
        )

        # Condition :
        #   1. Public User have group
        # Add Group Reject
        self.public_user.groups_id = [(
            4,
            grp_reject.id,
        )]
        # Add Group Reset
        self.public_user.groups_id = [(
            4,
            grp_reset.id
        )]

        # Result
        #   1. Public User can Request Approval
        #   2. Public User can Approve
        #   3. Public User can Reject
        #   4. Public User can Reset
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).request_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).approve_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reject_ok
        )
        self.assertEqual(
            True,
            purchase_request.sudo(
                self.public_user.id).reset_ok
        )
