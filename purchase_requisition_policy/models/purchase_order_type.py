# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    sent_supplier_group_ids = fields.Many2many(
        string="Allowed to Confirm Call",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_sent_supplier",
        col1="type_id",
        col2="group_id",
    )
    open_bid_group_ids = fields.Many2many(
        string="Allowed to Close Call for Bids",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_open_bid",
        col1="type_id",
        col2="group_id",
    )
    tender_reset_group_ids = fields.Many2many(
        string="Allowed to Reset to Draft",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_tender_reset",
        col1="type_id",
        col2="group_id",
    )
    open_product_group_ids = fields.Many2many(
        string="Allowed to Choose product lines",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_open_product",
        col1="type_id",
        col2="group_id",
    )
    generate_po_group_ids = fields.Many2many(
        string="Allowed to Done",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_generate_po",
        col1="type_id",
        col2="group_id",
    )
    cancel_requisition_group_ids = fields.Many2many(
        string="Allowed to Cancel Call",
        comodel_name="res.groups",
        rel="rel_purchase_requisition_cancel",
        col1="type_id",
        col2="group_id",
    )
