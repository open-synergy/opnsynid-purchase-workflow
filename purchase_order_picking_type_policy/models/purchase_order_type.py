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
