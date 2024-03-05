from odoo import api, fields, models


class StockPickings(models.Model):
    _inherit = "stock.picking"

    volume = fields.Integer(string="Volume", compute="_compute_volume", store=True)

    @api.depends("product_id")
    def _compute_volume(self):
        """
        this compute method will calculate the total volume of the batch
        from move ids which is in stock.picking model
        """
        total = 0
        for record in self:
            if record.move_ids:
                total = 0
                for i in record.move_ids:
                    total += i.product_id.volume * i.quantity

            record.volume = total
