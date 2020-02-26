# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class PurchaseOrderAnalysis(models.Model):
    _name = "purchase.order_analysis"
    _description = "Purchase Order Analysis"
    _auto = False
    _order = "date desc"

    order_id = fields.Many2one(
        string="#PO",
        comodel_name="purchase.order",
        readonly=True,
    )
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
    shipped = fields.Boolean(
        string="Received",
        readonly=True,
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
            MIN(l.id) AS id,
            s.id AS order_id,
            s.date_order AS date,
            l.state,
            s.date_approve,
            s.minimum_planned_date AS expected_date,
            s.dest_address_id,
            s.pricelist_id,
            s.validator,
            spt.warehouse_id AS picking_type_id,
            s.partner_id AS partner_id,
            s.create_uid AS user_id,
            s.company_id AS company_id,
            l.product_id,
            t.categ_id AS category_id,
            t.uom_id AS product_uom,
            s.location_id AS location_id,
            count(*) AS nbr,
            s.shipped AS shipped,
            rp.commercial_partner_id as commercial_partner_id,
            SUM(l.product_qty/u.factor*u2.factor) AS quantity,
            EXTRACT(
                epoch
                FROM age(s.date_approve,s.date_order)
            ) / (24*60*60)::decimal(16,2) AS delay,
            EXTRACT(
                epoch FROM age(l.date_planned,s.date_order)
            ) / (24*60*60)::decimal(16,2) AS delay_pass,
            SUM(
                l.price_unit/cr.rate * l.product_qty
            )::decimal(16,2) AS price_total,
            AVG(
                100.0 * (l.price_unit/cr.rate * l.product_qty) / NULLIF(
                    ip.value_float * l.product_qty/u.factor*u2.factor, 0.0
                )
            )::decimal(16,2) AS negociation,
            SUM(
                ip.value_float * l.product_qty / u.factor*u2.factor
            )::decimal(16,2) AS price_standard,
            (SUM(
                l.product_qty * l.price_unit / cr.rate
            ) / NULLIF(
                SUM(
                    l.product_qty / u.factor * u2.factor
                ),0.0)
            )::decimal(16,2) AS price_average
        """
        return select_str

    def _from(self):
        from_str = """
        FROM purchase_order_line l
        """
        return from_str

    def _join(self):
        join_str = """
        JOIN purchase_order AS s
            ON l.order_id = s.id
        LEFT JOIN product_product AS p
            ON l.product_id = p.id
        LEFT JOIN product_template AS t
            ON p.product_tmpl_id = t.id
        LEFT JOIN ir_property AS ip
            ON ip.name = 'standard_price'
            AND ip.res_id = CONCAT('product.template,',t.id)
            AND ip.company_id = s.company_id
        LEFT JOIN product_uom AS u
            ON u.id = l.product_uom
        LEFT JOIN product_uom AS u2
            ON u2.id = t.uom_id
        LEFT JOIN stock_picking_type AS spt
            ON spt.id = s.picking_type_id
        JOIN currency_rate AS cr
            ON cr.currency_id = s.currency_id
            AND cr.date_start <= coalesce(s.date_order, now())
            AND (cr.date_end is null or cr.date_end > coalesce(s.date_order, now()))
        JOIN res_partner AS rp
            ON s.partner_id = rp.id
        """
        return join_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _group_by(self):
        group_str = """
        GROUP BY
            s.id,
            s.company_id,
            s.create_uid,
            s.partner_id,
            u.factor,
            s.location_id,
            s.shipped,
            l.price_unit,
            s.date_approve,
            l.date_planned,
            l.product_uom,
            s.minimum_planned_date,
            s.pricelist_id,
            s.validator,
            s.dest_address_id,
            l.product_id,
            t.categ_id,
            s.date_order,
            l.state,
            spt.warehouse_id,
            u.uom_type,
            u.category_id,
            t.uom_id,
            u.id,
            u2.factor,
            rp.commercial_partner_id
        """
        return group_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            WITH currency_rate (currency_id, rate, date_start, date_end) AS (
                SELECT r.currency_id, r.rate, r.name AS date_start,
                    (SELECT name FROM res_currency_rate r2
                    WHERE r2.name > r.name AND
                        r2.currency_id = r.currency_id
                     ORDER BY r2.name ASC
                     LIMIT 1) AS date_end
                FROM res_currency_rate r
            )
            %s
            %s
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
