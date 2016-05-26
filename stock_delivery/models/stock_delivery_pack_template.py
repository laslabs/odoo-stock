# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
import openerp.addons.decimal_precision as dp


class StockDeliveryPackTemplate(models.Model):
    _name = 'stock.delivery.pack.template'
    _description = 'Stock Delivery Pack Template'

    name = fields.Char(required=True)
    length = fields.Float(
        digits=dp.get_precision('Pack Dimension'),
        required=True,
    )
    length_uom_id = fields.Many2one(
        string='Length Unit',
        comodel_name='product.uom',
        required=True,
    )
    width = fields.Float(
        digits=dp.get_precision('Pack Dimension'),
        required=True,
    )
    width_uom_id = fields.Many2one(
        string='Width Unit',
        comodel_name='product.uom',
        required=True,
    )
    height = fields.Float(
        digits=dp.get_precision('Pack Dimension'),
        required=True,
    )
    height_uom_id = fields.Many2one(
        string='Height Unit',
        comodel_name='product.uom',
        required=True,
    )
    weight = fields.Float(
        digits=dp.get_precision('Stock Weight'),
    )
    weight_uom_id = fields.Many2one(
        string='Weight Unit',
        comodel_name='product.uom',
    )
    active = fields.Boolean(
        default=True,
    )

    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Template name must be unique.')
    ]
