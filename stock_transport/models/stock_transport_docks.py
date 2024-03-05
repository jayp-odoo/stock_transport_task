from odoo import api, fields, models


class Docks(models.Model):
    """
    this models stores the information about of just name of the docks
    """

    _name = "stock.transport.docks"
    _description = "this stores information about docks"

    name = fields.Char(string="Name")
