{
    'name': 'Instafeed',
    'version': '1.0.0',
    'category': 'Sale',
    'author': 'Dat',
    'sequence': -101,
    'summary': 'Hospital management system',
    'description': """Hospital management system""",
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/config_setting.xml',
        'views/templates.xml',
        'data/cron_job.xml',
        'views/app.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {
        'instafeed.instafeed_js_package_assets': [
            'instafeed/static/js/index.js',
        ],
    }
}
