# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    limit_picking_type_selection = fields.Boolean(
        string="Limit Picking Type Selection",
    )
    allowed_picking_type_ids = fields.Many2many(
        string="Allowed Picking Type",
        comodel_name="stock.picking.type",
        relation="rel_po_type_2_pick_type",
        col1="type_id",
        col2="picking_type_id",
    )
    limit_picking_type_on_po = fields.Boolean(
        string="Limit Picking Type Selection on PO",
    )
    po_picking_type_policy_ids = fields.One2many(
        string="PO's Picking Type Policy",
        comodel_name="purchase.type_po_picking_type_policy",
        inverse_name="purchase_type_id",
    )


class PurchaseOrderTypePickingTypePolicy(models.Model):
    _name = "purchase.type_po_picking_type_policy"
    _description = "PO's Type Picking Type Policy"

    purchase_type_id = fields.Many2one(
        string="Purchase Type",
        comodel_name="purchase.order.type",
    )
    picking_type_id = fields.Many2one(
        string="Picking Type",
        comodel_name="stock.picking.type",
    )
    allowed_group_ids = fields.Many2many(
        string="Allowed Groups",
        comodel_name="res.groups",
        relation="po_type_picking_type_policy_rel",
        column1="policy_id",
        column2="group_id",
    )
