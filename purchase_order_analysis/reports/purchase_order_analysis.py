# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class PurchaseOrderAnalysis(models.Model):
    _name = "purchase.order_analysis"
    _description = "Purchase Order Analysis"
    _auto = False
    _order = "date desc"

    date = fields.Datetime(
        string="Order Date",
        readonly=True,
        help="Date on which this document has been created"
    )
    state = fields.Selection(
        string="Order Status",
        readonly=True,
        selection=[
            ("draft", "Request for Quotation"),
            ("confirmed", "Waiting Supplier Ack"),
            ("approved", "Approved"),
            ("except_picking", "Shipping Exception"),
            ("except_invoice", "Invoice Exception"),
            ("done", "Done"),
            ("cancel", "Cancelled")
        ]
    )
    product_id = fields.Many2one(
        string="Product",
        readonly=True,
        comodel_name="product.product"
    )
    picking_type_id = fields.Many2one(
        string="Warehouse",
        readonly=True,
        comodel_name="stock.warehouse"
    )
    location_id = fields.Many2one(
        string="Destination",
        readonly=True,
        comodel_name="stock.location"
    )
    partner_id = fields.Many2one(
        string="Supplier",
        readonly=True,
        comodel_name="res.partner"
    )
    commercial_partner_id = fields.Many2one(
        string="Supplier Commercial Partner",
        readonly=True,
        comodel_name="res.partner"
    )
    pricelist_id = fields.Many2one(
        string="Pricelist",
        readonly=True,
        comodel_name="product.pricelist"
    )
    date_approve = fields.Date(
        string="Date Approved",
        readonly=True
    )
    expected_date = fields.Date(
        string="Expected Date",
        readonly=True
    )
    validator = fields.Many2one(
        string="Validated By",
        readonly=True,
        comodel_name="res.users"
    )
    product_uom = fields.Many2one(
        string="Reference Unit of Measure",
        readonly=True,
        comodel_name="product.uom"
    )
    company_id = fields.Many2one(
        string="Company",
        readonly=True,
        comodel_name="res.company"
    )
    user_id = fields.Many2one(
        string="Responsible",
        readonly=True,
        comodel_name="res.users"
    )
    delay = fields.Float(
        string="Days to Validate",
        digits=(16, 2),
        readonly=True
    )
    delay_pass = fields.Float(
        string="Days to Deliver",
        digits=(16, 2),
        readonly=True
    )
    quantity = fields.Integer(
        string="Unit Quantity",
        readonly=True
    )
    price_total = fields.Float(
        string="Total Price",
        readonly=True
    )
    price_average = fields.Float(
        string="Average Price",
        readonly=True,
        group_operator="avg"
    )
    negociation = fields.Float(
        string="Purchase-Standard Price",
        readonly=True,
        group_operator="avg"
    )
    price_standard = fields.Float(
        string="Products Value",
        readonly=True,
        group_operator="sum"
    )
    nbr = fields.Integer(
        "# of Lines",
        readonly=True
    )
    category_id = fields.Many2one(
        string="Category",
        comodel_name="product.category",
        readonly=True
    )

    def _select(self):
        select_str = """
        SELECT
            a.id as id,
            a.date as date,
            a.state as state,
            a.product_id as product_id,
            a.picking_type_id as picking_type_id,
            a.location_id as location_id,
            a.partner_id as partner_id,
            b.commercial_partner_id as commercial_partner_id,
            a.pricelist_id as pricelist_id,
            a.date_approve as date_approve,
            a.expected_date as expected_date,
            a.validator as validator,
            a.product_uom as product_uom,
            a.company_id as company_id,
            a.user_id as user_id,
            a.delay as delay,
            a.delay_pass as delay_pass,
            a.quantity as quantity,
            a.price_total as price_total,
            a.price_average as price_average,
            a.negociation as negociation,
            a.price_standard as price_standard,
            a.nbr as nbr,
            a.category_id as category_id
        """
        return select_str

    def _from(self):
        from_str = """
        purchase_report AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN res_partner AS b
            ON a.partner_id = b.id
        """
        return join_str

    def _group_by(self):
        group_str = """
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where(),
            self._group_by()
        ))
