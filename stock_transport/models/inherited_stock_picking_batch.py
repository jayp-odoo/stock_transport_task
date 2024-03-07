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
    weight = fields.Float(string="Weight", compute="_compute_weight", store=True)
    volume = fields.Float(string="Volume", compute="_compute_volume", store=True)
    no_of_lines = fields.Integer(
        string="No of Lines", compute="_compute_no_of_lines", store=True
    )
    no_of_transfers = fields.Integer(
        string="No of Transfer", compute="_compute_no_of_transfers", store=True
    )

    @api.depends("move_line_ids")
    def _compute_no_of_lines(self):
        """
        this compute method is used to obtain the numbre of move lines
        in model data to be used in graph measurements
        """
        total_line = 0
        for record in self:
            if record.move_line_ids:
                total_line = len(record.move_line_ids)
        self.no_of_lines = total_line

    @api.depends("picking_ids")
    def _compute_no_of_transfers(self):
        """
        this compute method is used to obtain the numbre of picking lines lines
        in model data to be used in graph measurements
        """
        total = 0
        for record in self:
            if record.picking_ids:
                total = len(record.picking_ids)
        self.no_of_transfers = total

    @api.depends("vehicle_category", "move_line_ids")
    def _compute_weight(self):
        """
        this compute method is used to fill progressbar data with the use of movelines of weights
        """
        for record in self:
            if record.vehicle_category:
                total_weight = 0
                for products in record.move_line_ids:
                    total_weight += products.product_id.weight * products.quantity
                record.weight = (
                    total_weight / record.vehicle_category.max_weight
                ) * 100
            else:
                record.weight = 0

    @api.depends("vehicle_category", "move_line_ids")
    def _compute_volume(self):
        """
        this compute method is used to fill progressbar data with the use of movelines of volume
        """
        for record in self:
            if record.vehicle_category:
                total_weight = 0
                for products in record.move_line_ids:
                    total_weight += products.product_id.volume * products.quantity
                record.volume = (
                    total_weight / record.vehicle_category.max_volume
                ) * 100
            else:
                record.volume = 0

    @api.depends("vehicle", "weight", "volume")
    def _compute_display_name(self):
        """
        this method overwrite the display name of the vehicle model category
        """
        for record in self:
            name = record.name
            total_weight = 0
            total_volume = 0
            if record.move_line_ids:
                for products in record.move_line_ids:
                    total_weight += products.product_id.weight * products.quantity
                    total_volume += products.product_id.volume * products.quantity
                name = f"{record.vehicle.driver_id.name}: {total_weight}kg, {total_volume}m\u00B3"
            elif record.vehicle:
                name = record.vehicle.driver_id.name
            record.display_name = name
