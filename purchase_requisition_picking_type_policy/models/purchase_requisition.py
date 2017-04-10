# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.depends(
        "order_type",
        "order_type.allowed_picking_type_ids")
    def _compute_allowed_picking_type_ids(self):
        obj_type = self.env["stock.picking.type"]
        for pr in self:
            if pr.order_type.limit_picking_type_selection:
                pr.allowed_picking_type_ids = \
                    pr.order_type.allowed_picking_type_ids
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

    @api.onchange("order_type")
    def onchange_order_type(self):
        self.picking_type_id = False
        if self.allowed_picking_type_ids:
            self.picking_type_id = self.allowed_picking_type_ids[0]
