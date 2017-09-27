# -*- coding: utf-8 -*-
# 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Purchase Order Product Policy",
    "version": "8.0.2.1.0",
    "category": "Purchase",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "base_action_rule",
        "purchase_order_type_extension",
    ],
    "data": [
        "data/ir_actions_server_data.xml",
        "data/base_action_rule_data.xml",
        "views/purchase_order_type_views.xml",
        "views/purchase_order_views.xml",
    ],
}
