# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Request to RFQ Product Policy",
    "version": "8.0.1.1.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "auto_install": True,
    "depends": [
        "purchase_request_product_policy",
        "purchase_request_type_to_rfq",
    ],
    "data": [
        "wizard/purchase_request_line_make_purchase_order_view.xml",
    ],
}
