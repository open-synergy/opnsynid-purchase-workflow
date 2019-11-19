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
                    "allowed_product_ids": [
                        (6, 0, order_type.allowed_product_ids.ids)],
                    "allowed_product_categ_ids": [
                        (6, 0, order_type.allowed_product_categ_ids.ids)],
                })
            else:
                obj_product = self.env["product.product"]
                criteria = [
                    ("purchase_ok", "=", True),
                ]
                res.update({
                    "allowed_product_ids": [
                        (6, 0, obj_product.search(criteria).ids)],
                })
        return res


class PurchaseRequestLineMakePurchaseRequisitionItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.requisition.item"

    @api.multi
    @api.depends(
        "line_id",
        "line_id.request_id",
        "line_id.request_id.order_type_id",
    )
    def _compute_allowed_product(self):
        obj_product = self.env["product.product"]
        for document in self:
            type_id =\
                document.line_id.request_id.order_type_id

            if type_id.limit_product_selection:
                document.allowed_product_ids = \
                    type_id.allowed_product_ids.ids
                document.allowed_product_categ_ids = \
                    type_id.allowed_product_categ_ids.ids
            else:
                document.allowed_product_ids = \
                    obj_product.search([("purchase_ok", "=", True)])

    allowed_product_ids = fields.Many2many(
        string="Allowed Products",
        comodel_name="product.product",
        compute="_compute_allowed_product",
        store=False,
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        compute="_compute_allowed_product",
        store=False,
    )
