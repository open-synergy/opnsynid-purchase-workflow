# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.depends(
        "order_type",
        "order_type.all_allowed_product_ids")
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for po in self:
            if po.order_type.limit_product_selection:
                po.all_allowed_product_ids = \
                    po.order_type.all_allowed_product_ids
            else:
                criteria = [
                    ("purchase_ok", "=", True),
                ]
                po.all_allowed_product_ids = \
                    obj_product.search(criteria)

    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=False,
    )
