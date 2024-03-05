from odoo import api, fields, models


class Docks(models.Model):
    _name = "stock.transport.docks"
    _description = "this stores information about docks"

    name = fields.Char(string="Name")
