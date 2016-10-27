# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api


class PurchaseRequest(models.Model):
    _inherit = 'purchase.request'

    STATES = {
        'to_approve': [('readonly', True)],
        'approved': [('readonly', True)],
        'rejected': [('readonly', True)]
    }

    @api.model
    def _default_order_type(self):
        return self.env['purchase.order.type'].search([], limit=1)

    order_type_id = fields.Many2one(
        comodel_name='purchase.order.type',
        states=STATES,
        string='Type',
        ondelete='restrict',
        default=_default_order_type
    )


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    order_type_id = fields.Many2one(
        comodel_name='purchase.order.type',
        string='Type',
        related='request_id.order_type_id',
        store=True,
        readonly=True,
    )
