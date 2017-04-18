# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Requisition Policy",
    "version": "8.0.1.0.0",
    "category": "Purchase Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_requisition_type",
        "purchase_order_type_extension"
    ],
    "data": [
        "views/purchase_requisition_type_views.xml",
        "views/purchase_requisition_views.xml",
    ],
}
