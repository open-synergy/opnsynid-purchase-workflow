# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _get_picking_in(self):
        return False

    @api.depends(
        "order_type",
        "order_type.allowed_picking_type_ids")
    def _compute_allowed_picking_type_ids(self):
        obj_type = self.env["stock.picking.type"]
        obj_policy = self.env["purchase.type_po_picking_type_policy"]
        group_ids = self.env.user.groups_id.ids
        for po in self:
            if po.order_type.limit_picking_type_on_po:
                criteria = [
                    ("purchase_type_id", "=", po.order_type.id),
                ]
                criteria1 = criteria + [("allowed_group_ids", "=", False)]
                policies1 = obj_policy.search(criteria1)
                po.allowed_picking_type_ids = \
                    policies1.mapped("picking_type_id")
                criteria2 = criteria + [("allowed_group_ids", "!=", False)]
                for policy in obj_policy.search(criteria2):
                    for group in policy.allowed_group_ids:
                        if group.id in group_ids:
                            po.allowed_picking_type_ids += \
                                policy.picking_type_id
            else:
                criteria = [
                    ("code", "=", "incoming"),
                ]
                po.allowed_picking_type_ids = \
                    obj_type.search(criteria)

    allowed_picking_type_ids = fields.Many2many(
        string="Allowed Picking Type",
        comodel_name="stock.picking.type",
        compute="_compute_allowed_picking_type_ids",
        store=False,
    )

    @api.onchange("order_type")
    def onchange_order_type(self):
        super(PurchaseOrder, self).onchange_order_type()
        if self.allowed_picking_type_ids:
            self.picking_type_id = self.allowed_picking_type_ids[0]

    @api.model
    def _prepare_po_policy_domain(self, type_id):
        _super = super(PurchaseOrder, self)
        result = _super._prepare_po_policy_domain(
            type_id)
        purchase_type = self.env["purchase.order.type"].browse([type_id])[0]
        if not purchase_type.limit_picking_type_on_po:
            return result

        picking_type_ids = []
        group_ids = self.env.user.groups_id.ids
        obj_policy = self.env["purchase.type_po_picking_type_policy"]
        criteria = [
            ("purchase_type_id", "=", type_id),
        ]
        criteria1 = criteria + [("allowed_group_ids", "=", False)]
        policies1 = obj_policy.search(criteria1)
        picking_type_ids = \
            policies1.mapped("picking_type_id.id")
        criteria2 = criteria + [("allowed_group_ids", "!=", False)]
        for policy in obj_policy.search(criteria2):
            for group in policy.allowed_group_ids:
                if group.id in group_ids:
                    picking_type_ids.append(policy.picking_type_id.id)
        if len(picking_type_ids) > 0:
            result.insert(0, "&")
            result.insert(2, ("picking_type_id", "in", picking_type_ids))
        return result
