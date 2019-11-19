# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PurchaseOrderType(models.Model):
    _inherit = "purchase.order.type"

    limit_product_selection = fields.Boolean(
        string="Limit Product Selection",
    )
    allowed_product_categ_ids = fields.Many2many(
        string="Allowed Product Categories",
        comodel_name="product.category",
        relation="product_category_purchase_order_type_rel",
        column1="purchase_order_type_id",
        column2="product_category_id",
    )
    allowed_product_ids = fields.Many2many(
        string="Allowed Product",
        comodel_name="product.product",
        domain=[("purchase_ok", "=", True)],
        relation="rel_po_type_2_product",
        column1="purchase_order_type_id",
        column2="product_product_id",
    )
