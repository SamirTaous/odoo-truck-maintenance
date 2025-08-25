{
    'name': "Truck Maintenance",
    'version': '16.0.1.0.0',
    'summary': "Manage truck fleet, maintenance, and vehicle operations.",
    'description': "A comprehensive module for truck fleet management including vehicle specifications, maintenance scheduling, and operational tracking.",
    'author': "Samir Taous",
    'category': 'Operations/Fleet',
    'depends': [
        'web',
        'base', 
        'fleet',  # For the 'fleet.vehicle' model
        'mail',   # For the chatter and activity features
        'maintenance',  # For maintenance requests
    ],
    'data': [
        # 1. Security (Load first)
        'security/ir.model.access.csv',
        # 2. Data (Sequences, etc.)
        'data/sequence_data.xml',
        # 3. Views (UI)
        'views/truck_vehicle_views.xml',
        'views/maintenance_request_views.xml',
        'views/truck_dashboard_views.xml',
        'views/actions.xml',
        'views/menus.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'assets': {
        'web.assets_backend': [
            # Stylesheet Files
            'truck_maintenance/static/src/css/truck_maintenance.css',
            # JavaScript Files
            'truck_maintenance/static/src/js/truck_ownership_tree.js',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}