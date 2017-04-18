# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.multi
    @api.depends(
        "state",
        "order_type.sent_supplier_group_ids",
        "order_type.open_bid_group_ids",
        "order_type.tender_reset_group_ids",
        "order_type.open_product_group_ids",
        "order_type.generate_po_group_ids",
        "order_type.cancel_requisition_group_ids"
    )
    def _compute_policy(self):
        user_id = self.env.user.id
        for requisition in self:
            order_type = requisition.order_type
            if user_id == SUPERUSER_ID or not order_type:
                requisition.sent_supplier_ok = True
                requisition.open_bid_ok = True
                requisition.tender_reset_ok = True
                requisition.open_product_ok = True
                requisition.generate_po_ok = True
                requisition.cancel_requisition_ok = True
                continue

            requisition.sent_supplier_ok =\
                self._button_policy(order_type, 'sent_supplier')
            requisition.open_bid_ok =\
                self._button_policy(order_type, 'open_bid')
            requisition.tender_reset_ok =\
                self._button_policy(order_type, 'tender_reset')
            requisition.open_product_ok =\
                self._button_policy(order_type, 'open_product')
            requisition.generate_po_ok =\
                self._button_policy(order_type, 'generate_po')
            requisition.cancel_requisition_ok =\
                self._button_policy(order_type, 'cancel_requisition')

    @api.model
    def _button_policy(self, order_type, button_type):
        user = self.env.user
        group_ids = user.groups_id.ids
        button_group_ids = []

        if button_type == 'sent_supplier':
            button_group_ids = order_type.sent_supplier_group_ids.ids
        elif button_type == 'open_bid':
            button_group_ids = order_type.open_bid_group_ids.ids
        elif button_type == 'tender_reset':
            button_group_ids = order_type.tender_reset_group_ids.ids
        elif button_type == 'open_product':
            button_group_ids = order_type.open_product_group_ids.ids
        elif button_type == 'generate_po':
            button_group_ids = order_type.generate_po_group_ids.ids
        elif button_type == 'cancel_requisition':
            button_group_ids = order_type.cancel_requisition_group_ids.ids

        if button_group_ids:
            if (set(button_group_ids) & set(group_ids)):
                result = True
            else:
                result = False
        else:
            result = True
        return result

    sent_supplier_ok = fields.Boolean(
        string="Can Confirm Call",
        compute="_compute_policy",
        store=False,
    )
    open_bid_ok = fields.Boolean(
        string="Can Close Call for Bids",
        compute="_compute_policy",
        store=False,
    )
    tender_reset_ok = fields.Boolean(
        string="Can Reset to Draft",
        compute="_compute_policy",
        store=False,
    )
    open_product_ok = fields.Boolean(
        string="Can Choose product lines",
        compute="_compute_policy",
        store=False,
    )
    generate_po_ok = fields.Boolean(
        string="Can Done",
        compute="_compute_policy",
        store=False,
    )
    cancel_requisition_ok = fields.Boolean(
        string="Can Cancel Call",
        compute="_compute_policy",
        store=False,
    )
