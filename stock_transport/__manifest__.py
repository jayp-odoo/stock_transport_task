{
    "name": "stock_tranport",
    "depends": ["fleet", "stock_picking_batch"],
    "data": [
        "security/ir.model.access.csv",
        "views/Inherit_fleet_vehicle_model_category_view.xml",
        "views/inherit_stock_picking_view.xml",
        "views/inherit_stock_picking_batch_view.xml",
    ],
    "installable": True,
    "application": True,
}
