# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = [
        "purchase.request",
        "base.sequence_document",
        "base.workflow_policy_object",
    ]

    @api.model
    def _get_default_name(self):
        return "/"

    @api.multi
    @api.depends(
        "company_id",
    )
    def _compute_policy(self):
        _super = super(PurchaseRequest, self)
        _super._compute_policy()

    name = fields.Char(
        default=_get_default_name
    )
    request_ok = fields.Boolean(
        string="Can Request Approval",
        compute="_compute_policy",
        store=False,
    )
    approve_ok = fields.Boolean(
        string="Can Approve",
        compute="_compute_policy",
        store=False,
    )
    reject_ok = fields.Boolean(
        string="Can Reject",
        compute="_compute_policy",
        store=False,
    )
    reset_ok = fields.Boolean(
        string="Can Reset",
        compute="_compute_policy",
        store=False,
    )

    @api.model
    def create(self, values):
        _super = super(PurchaseRequest, self)
        result = _super.create(values)
        result.write({
            "name": result._create_sequence(),
        })
        return result

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})
        self.ensure_one()
        default.update({
            "state": "draft",
            "name": self._create_sequence(),
        })
        return super(PurchaseRequest, self).copy(default)
