# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Request Type',
    'version': '8.0.2.0.0',
    'summary': 'Add order type to purchase request',
    'author': 'Michael Viriyananda, Andhitia Rama, '
              'OpenSynergy Indonesia',
    'website': 'https://opensynergy-indonesia.com',
    'category': 'Purchase Management',
    'depends': [
        'purchase_request',
        'purchase_order_type'
    ],
    'data': [
        'views/purchase_request_view.xml',
        'views/purchase_request_line_view.xml'
    ],
    'installable': True,
    'license': 'AGPL-3',
}
