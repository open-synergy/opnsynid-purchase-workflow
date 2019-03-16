# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    sequence_id = fields.Many2one(
        string="Sequence",
        comodel_name="ir.sequence",
        company_dependent=True,
    )
    request_group_ids = fields.Many2many(
        string="Allowed to Request Approval",
        comodel_name="res.groups",
        rel="rel_purchase_req_request",
        col1="type_id",
        col2="group_id",
    )
    approve_group_ids = fields.Many2many(
        string="Allowed to Approve",
        comodel_name="res.groups",
        rel="rel_purchase_req_approve",
        col1="type_id",
        col2="group_id",
    )
    reject_group_ids = fields.Many2many(
        string="Allowed to Reject",
        comodel_name="res.groups",
        rel="rel_purchase_req_reject",
        col1="type_id",
        col2="group_id",
    )
    reset_group_ids = fields.Many2many(
        string="Allowed to Reset",
        comodel_name="res.groups",
        rel="rel_purchase_req_reset",
        col1="type_id",
        col2="group_id",
    )
