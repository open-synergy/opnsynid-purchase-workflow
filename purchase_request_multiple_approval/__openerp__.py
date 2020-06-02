# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Request Multiple Approval",
    "summary": "Implement a multiple approval process based on tiers "
               "for Purchase Request",
    "version": "8.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_request",
        "base_multiple_approval",
    ],
    "data": [
        "views/purchase_request_views.xml",
    ],
}
