# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from openerp import models


class PurchaseRequest(models.Model):
    _name = "purchase.request"
    _inherit = [
        "purchase.request",
        "tier.validation",
    ]
    _state_from = ["to_approve"]
    _state_to = ["approved"]
