# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    limit_usage_on_po = fields.Boolean(
        string="Limit Usage on PO",
    )
    allowed_usage_po_group_ids = fields.Many2many(
        string="Allowed Groups",
        comodel_name="res.groups",
        relation="po_type_usage_group_rel",
        column1="po_type_id",
        column2="group_id",
    )

    bid_group_ids = fields.Many2many(
        string="Allowed to Bid Received",
        comodel_name="res.groups",
        rel="rel_purchase_order_bid",
        col1="type_id",
        col2="group_id",
    )
    send_emailrfq_group_ids = fields.Many2many(
        string="Allowed to Send RFQ by Email",
        comodel_name="res.groups",
        rel="rel_purchase_order_send_emailrfq",
        col1="type_id",
        col2="group_id",
    )
    resend_emailrfq_group_ids = fields.Many2many(
        string="Allowed to Re-Send RFQ by Email",
        comodel_name="res.groups",
        rel="rel_purchase_order_resend_emailrfq",
        col1="type_id",
        col2="group_id",
    )
    confirm_order_group_ids = fields.Many2many(
        string="Allowed to Confirm Order",
        comodel_name="res.groups",
        rel="rel_purchase_order_confirm_order",
        col1="type_id",
        col2="group_id",
    )
    manually_picking_group_ids = fields.Many2many(
        string="Allowed to Manually Corrected (Shipping Exception)",
        comodel_name="res.groups",
        rel="rel_purchase_order_manually_picking",
        col1="type_id",
        col2="group_id",
    )
    manually_invoice_group_ids = fields.Many2many(
        string="Allowed to Manually Corrected (Invoice Exception)",
        comodel_name="res.groups",
        rel="rel_purchase_order_manually_invoice",
        col1="type_id",
        col2="group_id",
    )
    approve_order_group_ids = fields.Many2many(
        string="Allowed to Approve Order",
        comodel_name="res.groups",
        rel="rel_purchase_order_approve",
        col1="type_id",
        col2="group_id",
    )
    send_emailpo_group_ids = fields.Many2many(
        string="Allowed to Send PO by Email",
        comodel_name="res.groups",
        rel="rel_purchase_order_send_emailpo",
        col1="type_id",
        col2="group_id",
    )
    receive_prod_group_ids = fields.Many2many(
        string="Allowed to Receive Products",
        comodel_name="res.groups",
        rel="rel_purchase_order_receive_prod",
        col1="type_id",
        col2="group_id",
    )
    receive_inv_group_ids = fields.Many2many(
        string="Allowed to Receive Invoice",
        comodel_name="res.groups",
        rel="rel_purchase_order_receive_inv",
        col1="type_id",
        col2="group_id",
    )
    settodraft_order_group_ids = fields.Many2many(
        string="Allowed to Set To Draft",
        comodel_name="res.groups",
        rel="rel_purchase_order_settodraft_order",
        col1="type_id",
        col2="group_id",
    )
    cancel_order_group_ids = fields.Many2many(
        string="Allowed to Cancel",
        comodel_name="res.groups",
        rel="rel_purchase_order_cancel_order",
        col1="type_id",
        col2="group_id",
    )
