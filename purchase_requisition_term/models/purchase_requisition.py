# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    term_ids = fields.Many2many(
        string="Term(s)",
        comodel_name="purchase.term",
        column1="pr_id",
        column2="term_id",
    )

    @api.model
    def _prepare_purchase_order(self, requisition, supplier):
        res = super(PurchaseRequisition, self)._prepare_purchase_order(
            requisition, supplier)

        if requisition.term_ids:
            term_ids = []
            for term in requisition.term_ids:
                term_ids.append(term.id)
            res.update({'term_ids': [(6, 0, term_ids)]})

        return res
