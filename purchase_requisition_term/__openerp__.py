# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Requisition Term",
    "summary": "Add terms to purchase requisition",
    "version": "8.0.1.0.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_requisition",
        "purchase_order_term",
    ],
    "data": [
        "views/purchase_requisition_views.xml",
    ],
}
