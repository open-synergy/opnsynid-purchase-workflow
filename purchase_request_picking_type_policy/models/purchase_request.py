# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    @api.depends(
        "order_type_id",
        "order_type_id.allowed_picking_type_ids")
    def _compute_allowed_picking_type_ids(self):
        obj_type = self.env["stock.picking.type"]
        for pr in self:
            if pr.order_type_id.limit_picking_type_selection:
                pr.allowed_picking_type_ids = \
                    pr.order_type_id.allowed_picking_type_ids
            else:
                criteria = [
                    ("code", "=", "incoming"),
                ]
                pr.allowed_picking_type_ids = \
                    obj_type.search(criteria)

    allowed_picking_type_ids = fields.Many2many(
        string="Allowed Picking Type",
        comodel_name="stock.picking.type",
        compute="_compute_allowed_picking_type_ids",
        store=False,
    )

    @api.onchange("order_type_id")
    def onchange_order_type(self):
        self.picking_type_id = False
        if self.allowed_picking_type_ids:
            self.picking_type_id = self.allowed_picking_type_ids[0]
