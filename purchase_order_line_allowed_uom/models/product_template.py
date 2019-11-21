# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    limit_product_uom_selection = fields.Boolean(
        string="Limit Product UoM Selection",
    )

    @api.multi
    @api.depends(
        "uom_id"
    )
    def _compute_allowed_product_uom_categ_id(self):
        for document in self:
            if document.uom_id:
                document.allowed_product_uom_categ_id = \
                    document.uom_id.category_id.id

    allowed_product_uom_categ_id = fields.Many2one(
        string="Allowed Product UoM Category",
        comodel_name="product.uom.categ",
        compute="_compute_allowed_product_uom_categ_id",
        store=False,
    )
    allowed_purchase_uom_ids = fields.Many2many(
        string="Allowed Purchase UoM",
        comodel_name="product.uom",
        relation="rel_product_allowed_purchase_uom",
        column1="product_id",
        column2="uom_id"
    )
