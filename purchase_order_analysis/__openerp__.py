# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Analysis",
    "version": "8.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase"
    ],
    "data": [
        "security/ir.model.access.csv",
        "reports/purchase_order_analysis.xml"
    ],
}
