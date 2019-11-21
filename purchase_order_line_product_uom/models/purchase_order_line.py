# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.multi
    @api.depends(
        "product_id",
    )
    def _compute_product_uom_id(self):
        for document in self:
            document.product_uom_id = False
            if document.product_id:
                document.product_uom_id =\
                    document.product_id.uom_id.id

    product_uom_id = fields.Many2one(
        string="Product UoM",
        comodel_name="product.uom",
        compute="_compute_product_uom_id",
        store=True,
    )

    @api.multi
    @api.depends(
        "product_uom_id",
        "product_uom",
        "product_qty",
    )
    def _compute_product_uom_qty(self):
        for document in self:
            document.product_uom_qty = 0.0
            if document.product_uom_id:
                document.product_uom_qty =\
                    document.product_uom_id._compute_qty(
                        from_uom_id=document.product_uom.id,
                        to_uom_id=document.product_uom_id.id,
                        qty=document.product_qty)

    product_uom_qty = fields.Float(
        string="Product UoM Qty",
        compute="_compute_product_uom_qty",
        store=True,
    )
