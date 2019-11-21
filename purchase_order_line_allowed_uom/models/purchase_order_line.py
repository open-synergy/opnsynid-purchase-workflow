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
    def _compute_allowed_purchase_uom_ids(self):
        obj_product_uom =\
            self.env["product.uom"]
        for document in self:
            uom_po = document.product_id.uom_po_id
            if document.product_id:
                if document.product_id.limit_product_uom_selection:
                    allowed_purchase_uom_ids =\
                        document.product_id.allowed_purchase_uom_ids.ids
                    if uom_po.id not in allowed_purchase_uom_ids:
                        allowed_purchase_uom_ids.append(uom_po.id)
                    document.allowed_purchase_uom_ids =\
                        allowed_purchase_uom_ids
                else:
                    category_id =\
                        uom_po.category_id.id
                    criteria = [
                        ("category_id", "=", category_id)
                    ]
                    document.allowed_purchase_uom_ids =\
                        obj_product_uom.search(criteria)

    allowed_purchase_uom_ids = fields.Many2many(
        string="Allowed Invoices",
        comodel_name="product.uom",
        compute="_compute_allowed_purchase_uom_ids",
        store=False,
    )

    @api.onchange(
        "product_id",
        "product_uom",
        "product_qty",
    )
    @api.depends(
        "order_id.pricelist_id",
        "product_id",
        "product_qty",
        "product_uom",
        "order_id.partner_id",
        "order_id.date_order",
        "order_id.fiscal_position",
        "date_planned",
        "name",
        "order_id.state",
    )
    def onchange_product_id_new_api(self):
        _super = super(PurchaseOrderLine, self)
        result = _super.onchange_product_id(
            self.order_id.pricelist_id.id,
            self.product_id.id,
            self.product_qty,
            self.product_uom.id,
            self.order_id.partner_id.id,
            self.order_id.date_order,
            self.order_id.fiscal_position.id,
            self.date_planned,
            self.name,
            False,
            self.order_id.state,
        )

        if type(result) is dict and "value" in result:
            for field, value in result.get('value').items():
                if hasattr(self, field):
                    setattr(self, field, value)
