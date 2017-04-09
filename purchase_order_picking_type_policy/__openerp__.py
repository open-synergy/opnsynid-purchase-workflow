# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Picking Type Policy",
    "version": "8.0.1.0.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_order_type_extension",
    ],
    "data": [
        "views/purchase_order_type_views.xml",
        "views/purchase_order_views.xml",
    ],
}
