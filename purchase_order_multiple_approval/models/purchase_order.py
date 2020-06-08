# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import models, fields, api


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = [
        "purchase.order",
        "tier.validation",
    ]
    _state_from = [
        "draft",
        "confirmed"
    ]
    _state_to = [
        "approved",
    ]

    STATE_SELECTION = [
        ("draft", "Draft PO"),
        ("sent", "RFQ"),
        ("bid", "Bid Received"),
        ("confirmed", "Waiting for Approval"),
        ("approved", "Purchase Approved"),
        ("except_picking", "Shipping Exception"),
        ("except_invoice", "Invoice Exception"),
        ("done", "Done"),
        ("cancel", "Cancelled")
    ]

    state = fields.Selection(
        string="Status",
        selection=STATE_SELECTION,
        readonly=True,
        select=True,
        copy=False,
      )

    @api.multi
    def wkf_confirm_order(self):
        _super = super(PurchaseOrder, self)
        _super.wkf_confirm_order()
        for document in self:
            document.request_validation()

    @api.multi
    def wkf_action_cancel(self):
        _super = super(PurchaseOrder, self)
        _super.wkf_action_cancel()
        for document in self:
            document.restart_validation()

    @api.multi
    def validate_tier(self):
        _super = super(PurchaseOrder, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.wkf_approve_order()

    @api.multi
    def restart_validation(self):
        _super = super(PurchaseOrder, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()
