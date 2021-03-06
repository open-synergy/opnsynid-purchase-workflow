# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Request Line Department",
    "version": "8.0.1.0.0",
    "category": "Purchase Request",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_request",
        "hr"
    ],
    "data": [
        "views/purchase_request_views.xml",
        "views/purchase_request_line_views.xml"
    ],
}
