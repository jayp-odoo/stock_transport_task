from odoo import api, fields, models


class StockPickingBatch(models.Model):
    """
    this class is inherited from stock.picking.batch to add some fields and computed methods
    """

    _inherit = "stock.picking.batch"

    dock_id = fields.Many2one("stock.transport.docks", string="Dock")
    # forgot to add name as vehicle_id
    vehicle = fields.Many2one("fleet.vehicle", string="Vehicle")
    # forgot to add name as vehicle_category_id
    vehicle_category = fields.Many2one(
        "fleet.vehicle.model.category",
        string="Vehicle Category",
    )
    weight = fields.Integer(string="Weight", compute="_compute_weight")
    volume = fields.Integer(string="Volume", compute="_compute_volume")

    @api.depends("vehicle_category", "picking_ids")
    def _compute_weight(self):
        for record in self:
            current_total_weight = 0
            if record.picking_ids:

                current_total_weight = sum(record.picking_ids.mapped("weight"))
            if current_total_weight > 0 and record.vehicle_category.max_weight > 0:
                record.weight = (
                    current_total_weight * 100
                ) / record.vehicle_category.max_weight
            else:
                record.weight = 0

    @api.depends("vehicle_category", "picking_ids")
    def _compute_volume(self):
        for record in self:
            current_total_volume = 0
            if record.picking_ids:

                current_total_volume = sum(record.picking_ids.mapped("volume"))
            if current_total_volume > 0 and record.vehicle_category.max_volume > 0:
                record.volume = (
                    current_total_volume * 100
                ) / record.vehicle_category.max_volume
            else:
                record.volume = 0
