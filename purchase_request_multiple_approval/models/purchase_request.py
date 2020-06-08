# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import models, api


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = [
        "purchase.request",
        "tier.validation",
    ]
    _state_from = [
        "draft",
        "to_approve"
    ]
    _state_to = [
        "approved",
    ]

    @api.multi
    def button_to_approve(self):
        _super = super(PurchaseRequest, self)
        _super.button_to_approve()
        for document in self:
            document.request_validation()

    @api.multi
    def button_rejected(self):
        _super = super(PurchaseRequest, self)
        _super.button_rejected()
        for document in self:
            document.restart_validation()

    @api.multi
    def validate_tier(self):
        _super = super(PurchaseRequest, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.button_approved()

    @api.multi
    def restart_validation(self):
        _super = super(PurchaseRequest, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()
