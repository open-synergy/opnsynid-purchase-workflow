# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.request.line"

    department_id = fields.Many2one(
        string="Department",
        comodel_name="hr.department",
    )
