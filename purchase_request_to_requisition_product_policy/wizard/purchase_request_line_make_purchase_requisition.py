# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields


class PurchaseRequestLineMakePurchaseRequisition(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition"

    @api.model
    def _prepare_item(self, line):
        res = super(PurchaseRequestLineMakePurchaseRequisition, self)\
            ._prepare_item(line)
        order_type_id = res.get("order_type_id", False)
        if order_type_id:
            obj_type = self.env["purchase.order.type"]
            order_type = obj_type.browse(order_type_id)
            if order_type.limit_product_selection:
                res.update({
                    "all_allowed_product_ids": [
                        (6, 0, order_type.all_allowed_product_ids.ids)],
                })
            else:
                obj_product = self.env["product.product"]
                criteria = [
                    ("purchase_ok", "=", True),
                ]
                res.update({
                    "all_allowed_product_ids": [
                        (6, 0, obj_product.search(criteria).ids)],
                })
        return res


class PurchaseRequestLineMakePurchaseRequisitionItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition.item"

    @api.depends(
        "line_id",
        "line_id.request_id",
        "line_id.request_id.order_type_id",
        "line_id.request_id.order_type_id.all_allowed_product_ids")
    def _compute_all_allowed_product_ids(self):
        obj_product = self.env["product.product"]
        for line in self:
            if line.line_id.request_id.order_type_id.limit_product_selection:
                line.all_allowed_product_ids = \
                    line.line_id.request_id.order_type_id.\
                    all_allowed_product_ids
            else:
                criteria = [
                    ("purchase_ok", "=", True),
                ]
                line.all_allowed_product_ids = \
                    obj_product.search(criteria)

    all_allowed_product_ids = fields.Many2many(
        string="All Allowed Product",
        comodel_name="product.product",
        compute="_compute_all_allowed_product_ids",
        store=False,
    )
