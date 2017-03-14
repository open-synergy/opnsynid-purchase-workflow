# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    @api.multi
    @api.depends(
        "state",
        "order_type_id.request_group_ids",
        "order_type_id.approve_group_ids",
        "order_type_id.reject_group_ids",
        "order_type_id.reset_group_ids",
    )
    def _compute_policy(self):
        obj_purchase_order_type = self.env["purchase.order.type"]
        for purchase_req in self:
            if self.env.user.id == SUPERUSER_ID:
                purchase_req.request_ok = True
                purchase_req.approve_ok = True
                purchase_req.reject_ok = True
                purchase_req.reset_ok = True
                continue
            else:
                purchase_req.request_ok = False
                purchase_req.approve_ok = False
                purchase_req.reject_ok = False
                purchase_req.reset_ok = False

            purchase_req_id = purchase_req.order_type_id.id

            if not purchase_req_id:
                continue

            purchase_req_type =\
                obj_purchase_order_type.browse([purchase_req_id])[0]
            purchase_req.request_ok = self._request_policy(purchase_req_type)
            purchase_req.approve_ok = self._approve_policy(purchase_req_type)
            purchase_req.reject_ok = self._reject_policy(purchase_req_type)
            purchase_req.reset_ok = self._reset_policy(purchase_req_type)

    @api.model
    def _request_policy(self, purchase_req_type):
        result = False
        user = self.env.user
        request_group_ids = purchase_req_type.request_group_ids.ids
        group_ids = user.groups_id.ids
        if not purchase_req_type.request_group_ids.ids:
            result = True
        else:
            if (set(request_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _approve_policy(self, purchase_req_type):
        result = False
        user = self.env.user
        approve_group_ids = purchase_req_type.approve_group_ids.ids
        group_ids = user.groups_id.ids
        if not purchase_req_type.approve_group_ids.ids:
            result = True
        else:
            if (set(approve_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _reject_policy(self, purchase_req_type):
        result = False
        user = self.env.user
        reject_group_ids = purchase_req_type.reject_group_ids.ids
        group_ids = user.groups_id.ids
        if not purchase_req_type.reject_group_ids.ids:
            result = True
        else:
            if (set(reject_group_ids) & set(group_ids)):
                result = True
        return result

    @api.model
    def _reset_policy(self, purchase_req_type):
        result = False
        user = self.env.user
        reset_group_ids = purchase_req_type.reset_group_ids.ids
        group_ids = user.groups_id.ids
        if not purchase_req_type.reset_group_ids.ids:
            result = True
        else:
            if (set(reset_group_ids) & set(group_ids)):
                result = True
        return result

    request_ok = fields.Boolean(
        string="Can Request Approval",
        compute="_compute_policy",
        store=False,
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
        store=False,
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
        store=False,
    )
    reset_ok = fields.Boolean(
        string="Can Reset",
        compute="_compute_policy",
        store=False,
    )
