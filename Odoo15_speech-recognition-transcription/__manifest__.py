# -*- coding: utf-8 -*-

{
    'name': 'customer-service_skywalker',
    'version': '1.0.0',
    'summary': 'Customer Service Management',
    'sequence': -100,
    'description': """Call Center Agent - Case Logging Tool""",
    'category': 'Services',
    'author': 'Samet Çolak "Skywalker"',
    'license': 'AGPL-3',
    'depends': [
        'sale',
        'mail',
        'website_slides',
        'hr',
        'crm',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/client.xml',
    ],
    'demo': [],

    'images': ['C:/odoo-15.0/custom_addons/customerservice_skywalker/static/description/customer-services_auto.jpg'],
    'installable': True,
    'application': True,
    'auto_install': False,
}