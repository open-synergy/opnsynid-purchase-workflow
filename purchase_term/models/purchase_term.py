# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseTerm(models.Model):
    _name = "purchase.term"
    _description = "Purchase Term"

    @api.one
    @api.depends("code")
    def _compute_name(self):
        self.display_name = self.code

    name = fields.Char(
        string="Term",
        required=True,
    )
    code = fields.Char(
        string="Code",
        required=True,
    )
    display_name = fields.Char(
        string="Display Name",
        compute="_compute_name",
        store=False)
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    description = fields.Text(
        string="Description",
    )
