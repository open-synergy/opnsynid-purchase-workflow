# -*- coding: utf-8 -*-
# © 2016 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models, fields
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _
from lxml import etree


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    @api.model
    def _get_order_type(self):
        val = False
        obj_purchase_request_line = self.env['purchase.request.line']
        active_ids = self.env.context['active_ids'] or []

        for line in obj_purchase_request_line.browse(active_ids):
            if not val:
                val = line.order_type_id.id
            else:
                if line.order_type_id.id != val:
                    raise UserError(
                        _('You have to select lines '
                          'from the same type.'))
        return val

    @api.model
    def _prepare_item(self, line):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)\
            ._prepare_item(line)
        res.update({
            'order_type_id': line.order_type_id.id
        })
        return res

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)\
            .fields_view_get(
                view_id=view_id, view_type=view_type,
                toolbar=toolbar, submenu=submenu)

        order_type_id = self._get_order_type()

        if 'arch' in res:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='purchase_order_id']"):
                domain = "[('order_type', 'in', [%s])]" % order_type_id
                node.set('domain', domain)
            res['arch'] = etree.tostring(doc)
        return res

    @api.model
    def _prepare_purchase_order(self, picking_type, location, company_id):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)\
            ._prepare_purchase_order(
                picking_type, location, company_id)

        order_type_id = self._get_order_type()
        res.update({'order_type': order_type_id})

        return res


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    order_type_id = fields.Many2one(
        comodel_name='purchase.order.type',
        string='Type',
        related='line_id.request_id.order_type_id',
        store=True,
        readonly=True,
    )
