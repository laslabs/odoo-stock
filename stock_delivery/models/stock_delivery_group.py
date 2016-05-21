# -*- coding: utf-8 -*-
# © 2016-TODAY LasLabs Inc.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp
from openerp.addons.stock_delivery.models.stock_delivery_operation import (
    OPERATION_STATES,
)


class StockDeliveryGroup(models.Model):
    _name = 'stock.delivery.group'
    _description = 'Stock Delivery Group'

    picking_id = fields.Many2one(
        string='Stock Picking',
        comodel_name='stock.picking',
        required=True,
    )
    operation_ids = fields.One2many(
        string='Delivery Ops',
        comodel_name='stock.delivery.operation',
        inverse_name='group_id',
    )
    label_id = fields.Many2one(
        string='Delivery Label',
        comodel_name='stock.delivery.label',
    )
    pack_id = fields.Many2one(
        string='Delivery Pack',
        comodel_name='stock.delivery.pack',
    )
    move_id = fields.Many2one(
        string='Account Move',
        comodel_name='account.move',
    )
    last_operation_id = fields.Many2one(
        string='Last Delivery Op',
        comodel_name='stock.delivery.operation',
        compute='_compute_last_operation_id',
    )
    carrier_tracking_ref = fields.Char()
    state = fields.Selection(
        OPERATION_STATES,
        related='last_operation_id.state',
    )
    signed_by = fields.Char()
    carrier_weight = fields.Float(
        digits=dp.get_precision('Stock Weight'),
    )
    carrier_weight_uom_id = fields.Many2one(
        string='Carrier Weight Unit',
        comodel_name='product.uom',
    )
    date_delivery_est = fields.Datetime()
    service_id = fields.Many2one(
        string='Carrier Service',
        comodel_name='delivery.carrier',
        related='picking_id.carrier_id',
    )
    partner_id = fields.Many2one(
        string='Carrier Company',
        comodel_name='res.partner',
        related='service_id.partner_id',
    )

    @api.multi
    def _compute_last_operation_id(self):
        for rec_id in self:
            if len(rec_id.operation_ids):
                self.last_operation_id = rec_id.operation_ids.sorted(
                    key=lambda r: r.date_updated,
                )[-1]

    @api.model
    def create(self, vals):
        if not vals.get('carrier_tracking_ref'):
            picking_id = self.env['stock.picking'].browse(vals['picking_id'])
            vals['carrier_tracking_ref'] = picking_id.carrier_tracking_ref
        return super(StockDeliveryGroup, self).create(vals)