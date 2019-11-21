# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Line - Allowed Product Uom",
    "version": "8.0.1.0.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_order_line_product_uom",
    ],
    "data": [
        "views/product_template_views.xml",
        "views/purchase_order_views.xml",
        "views/purchase_order_line_views.xml",
    ],
}
