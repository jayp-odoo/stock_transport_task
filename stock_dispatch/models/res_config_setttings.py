from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    """
    this model inherits from ResConfigSettings to add new field module_stock_transport to the settings form
    """

    _inherit = "res.config.settings"

    module_stock_transport = fields.Boolean(
        "Dispatch Management System",
        help="Transport Management: organize packs in your fleet, or carriers.",
    )
