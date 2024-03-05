from odoo import api, fields, models


class FleetVehicleModelCategory(models.Model):
    """
    this class inherits fleet.vehicle.model.category to add two more fields like max_weight and max_valume
    """

    _inherit = "fleet.vehicle.model.category"

    max_weight = fields.Integer(string="Max Weight (kg)", default=0.0)
    max_volume = fields.Integer(string=f"Max Volume (m\u00B3)", default=0.0)

    @api.depends("name", "max_weight", "max_volume")
    def _compute_display_name(self):
        """
        this method overwrite the display name of the vehicle model category
        """
        for record in self:
            name = record.name
            if record.max_weight and record.max_volume:
                name = f"{name}({record.max_weight}kg, {record.max_volume}m\u00B3)"
            record.display_name = name
