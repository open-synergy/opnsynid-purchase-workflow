# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Picking Type Policy",
    "version": "8.0.2.1.1",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_order_policy",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_type_views.xml",
        "views/purchase_order_views.xml",
    ],
}
