# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.depends(
        "order_type",
        "order_type.all_allowed_product_ids")
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for pr in self:
            if pr.order_type.limit_product_selection:
                pr.all_allowed_product_ids = \
                    pr.order_type.all_allowed_product_ids
            else:
                criteria = [
                    ("purchase_ok", "=", True),
                ]
                pr.all_allowed_product_ids = \
                    obj_product.search(criteria)

    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=False,
    )
