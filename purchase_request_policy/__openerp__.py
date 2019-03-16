# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Request Policy",
    "version": "8.0.1.2.0",
    "category": "Purchase Management",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "purchase_request_type",
        "purchase_order_type_extension",
        "base_sequence_configurator",
        "base_workflow_policy",
    ],
    "data": [
        "data/base_sequence_configurator_data.xml",
        "data/base_workflow_policy_data.xml",
        "views/purchase_order_type_views.xml",
        "views/purchase_request_views.xml",
    ],
}
