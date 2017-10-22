# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api, fields, SUPERUSER_ID


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    @api.depends(
        "state",
        "order_type.bid_group_ids",
        "order_type.send_emailrfq_group_ids",
        "order_type.resend_emailrfq_group_ids",
        "order_type.confirm_order_group_ids",
        "order_type.manually_picking_group_ids",
        "order_type.manually_invoice_group_ids",
        "order_type.approve_order_group_ids",
        "order_type.send_emailpo_group_ids",
        "order_type.receive_prod_group_ids",
        "order_type.receive_inv_group_ids",
        "order_type.settodraft_order_group_ids",
        "order_type.cancel_order_group_ids"
    )
    def _compute_policy(self):
        obj_purchase_order_type = self.env["purchase.order.type"]
        for purchase_order in self:
            if self.env.user.id == SUPERUSER_ID:
                purchase_order.bid_ok = True
                purchase_order.send_emailrfq_ok = True
                purchase_order.resend_emailrfq_ok = True
                purchase_order.confirm_order_ok = True
                purchase_order.manually_picking_ok = True
                purchase_order.manually_invoice_ok = True
                purchase_order.approve_order_ok = True
                purchase_order.send_emailpo_ok = True
                purchase_order.receive_prod_ok = True
                purchase_order.receive_inv_ok = True
                purchase_order.settodraft_order_ok = True
                purchase_order.cancel_order_ok = True
                continue

            order_type_id = purchase_order.order_type.id

            if not order_type_id:
                purchase_order.bid_ok = True
                purchase_order.send_emailrfq_ok = True
                purchase_order.resend_emailrfq_ok = True
                purchase_order.confirm_order_ok = True
                purchase_order.manually_picking_ok = True
                purchase_order.manually_invoice_ok = True
                purchase_order.approve_order_ok = True
                purchase_order.send_emailpo_ok = True
                purchase_order.receive_prod_ok = True
                purchase_order.receive_inv_ok = True
                purchase_order.settodraft_order_ok = True
                purchase_order.cancel_order_ok = True
                continue

            order_type =\
                obj_purchase_order_type.browse([order_type_id])[0]
            purchase_order.bid_ok = self._button_policy(order_type, 'bid')
            purchase_order.send_emailrfq_ok =\
                self._button_policy(order_type, 'send_emailrfq')
            purchase_order.resend_emailrfq_ok =\
                self._button_policy(order_type, 'resend_emailrfq')
            purchase_order.confirm_order_ok =\
                self._button_policy(order_type, 'confirm_order')
            purchase_order.manually_picking_ok =\
                self._button_policy(order_type, 'manually_picking')
            purchase_order.manually_invoice_ok =\
                self._button_policy(order_type, 'manually_invoice')
            purchase_order.approve_order_ok =\
                self._button_policy(order_type, 'approve_order')
            purchase_order.send_emailpo_ok =\
                self._button_policy(order_type, 'send_emailpo')
            purchase_order.receive_prod_ok =\
                self._button_policy(order_type, 'receive_prod')
            purchase_order.receive_inv_ok =\
                self._button_policy(order_type, 'receive_inv')
            purchase_order.settodraft_order_ok =\
                self._button_policy(order_type, 'settodraft_order')
            purchase_order.cancel_order_ok =\
                self._button_policy(order_type, 'cancel_order')

    @api.model
    def _button_policy(self, order_type, button_type):
        result = False
        user = self.env.user
        group_ids = user.groups_id.ids

        if button_type == 'bid':
            button_group_ids = order_type.bid_group_ids.ids
        elif button_type == 'send_emailrfq':
            button_group_ids = order_type.send_emailrfq_group_ids.ids
        elif button_type == 'resend_emailrfq':
            button_group_ids = order_type.resend_emailrfq_group_ids.ids
        elif button_type == 'confirm_order':
            button_group_ids = order_type.confirm_order_group_ids.ids
        elif button_type == 'manually_picking':
            button_group_ids = order_type.manually_picking_group_ids.ids
        elif button_type == 'manually_invoice':
            button_group_ids = order_type.manually_invoice_group_ids.ids
        elif button_type == 'approve_order':
            button_group_ids = order_type.approve_order_group_ids.ids
        elif button_type == 'send_emailpo':
            button_group_ids = order_type.send_emailpo_group_ids.ids
        elif button_type == 'receive_prod':
            button_group_ids = order_type.receive_prod_group_ids.ids
        elif button_type == 'receive_inv':
            button_group_ids = order_type.receive_inv_group_ids.ids
        elif button_type == 'settodraft_order':
            button_group_ids = order_type.settodraft_order_group_ids.ids
        elif button_type == 'cancel_order':
            button_group_ids = order_type.cancel_order_group_ids.ids

        if not button_group_ids:
            result = True
        else:
            if (set(button_group_ids) & set(group_ids)):
                result = True
        return result

    bid_ok = fields.Boolean(
        string="Can Bid Received",
        compute="_compute_policy",
        store=False,
    )
    send_emailrfq_ok = fields.Boolean(
        string="Can Send RFQ by Email",
        compute="_compute_policy",
        store=False,
    )
    resend_emailrfq_ok = fields.Boolean(
        string="Can Re-Send RFQ by Email",
        compute="_compute_policy",
        store=False,
    )
    confirm_order_ok = fields.Boolean(
        string="Can Confirm Order",
        compute="_compute_policy",
        store=False,
    )
    manually_picking_ok = fields.Boolean(
        string="Can Manually Corrected (Shipping Exception)",
        compute="_compute_policy",
        store=False,
    )
    manually_invoice_ok = fields.Boolean(
        string="Can Manually Corrected (Invoice Exception)",
        compute="_compute_policy",
        store=False,
    )
    approve_order_ok = fields.Boolean(
        string="Can Approve Order",
        compute="_compute_policy",
        store=False,
    )
    send_emailpo_ok = fields.Boolean(
        string="Can Send PO by Email",
        compute="_compute_policy",
        store=False,
    )
    receive_prod_ok = fields.Boolean(
        string="Can Receive Products",
        compute="_compute_policy",
        store=False,
    )
    receive_inv_ok = fields.Boolean(
        string="Can Receive Invoice",
        compute="_compute_policy",
        store=False,
    )
    settodraft_order_ok = fields.Boolean(
        string="Can Set To Draft",
        compute="_compute_policy",
        store=False,
    )
    cancel_order_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
        store=False,
    )
    order_type = fields.Many2one(
        default=lambda self: self._default_order_type(),
    )

    @api.model
    def _default_order_type(self):
        return False

    @api.model
    def _search(
            self, args, offset=0, limit=None, order=None,
            count=False, access_rights_uid=None):
        _super = super(PurchaseOrder, self)
        limit_po_policy = self._context.get("po_policy", False)
        if limit_po_policy:
            policy_result = self._get_po_policy_domain()
            args += policy_result
        result = _super._search(
            args, offset=offset, limit=limit, order=order,
            count=count, access_rights_uid=access_rights_uid)
        return result

    @api.model
    def _get_po_policy_domain(self):
        group_ids = tuple(self.env.user.groups_id.ids)
        obj_type = self.env["purchase.order.type"]
        type_ids = []
        result = []
        criteria = [
            ("limit_usage_on_po", "=", False),
        ]
        type_ids += obj_type.search(criteria).ids
        criteria2 = [
            ("limit_usage_on_po", "=", True),
        ]
        for purchase_type in obj_type.search(criteria2):
            for group in purchase_type.allowed_group_ids:
                if group.id in group_ids:
                    type_ids.append(purchase_type.id)
        for type_count in range(0, len(type_ids)):
            dom = self._prepare_po_policy_domain(
                type_ids[type_count])
            if type_count > 0:
                result.insert(0, "|")
            result += dom
        return result

    @api.model
    def _prepare_po_policy_domain(self, type_id):
        result = [("order_type", "=", type_id)]
        return result

    @api.model
    def read_group(
            self, domain, fields, groupby, offset=0, limit=None,
            orderby=False, lazy=True):
        _super = super(PurchaseOrder, self)
        limit_po_policy = self._context.get("po_policy", False)
        if limit_po_policy:
            policy_result = self._get_po_policy_domain()
            domain += policy_result
        result = _super.read_group(
            domain=domain, fields=fields, groupby=groupby,
            offset=offset, limit=limit, orderby=orderby, lazy=lazy)
        return result
