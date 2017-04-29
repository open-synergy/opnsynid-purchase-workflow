# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Requisition Picking Type Policy",
    "version": "8.0.1.1.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_requisition_type",
        "purchase_order_picking_type_policy",
    ],
    "data": [
        "views/purchase_requisition_views.xml",
    ],
}
