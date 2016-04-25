# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    term_ids = fields.Many2many(
        string="Term(s)",
        comodel_name="purchase.term",
        column1="pr_line_id",
        column2="term_id",
    )


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.model
    def _prepare_purchase_order_line(self, requisition, requisition_line,
                                     purchase_id, supplier):
        res = super(PurchaseRequisition, self)._prepare_purchase_order_line(
            requisition, requisition_line, purchase_id, supplier)

        if requisition_line.term_ids:
            term_ids = []
            for term in requisition_line.term_ids:
                term_ids.append(term.id)
            res.update({'term_ids': [(6, 0, term_ids)]})

        return res
