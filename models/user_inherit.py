from odoo import models, fields

class UserInherit(models.Model):
    _inherit = 'res.users'

    shop_id = fields.One2many('shopify.shop','user_id')
    facebook_id = fields.One2many('facebook.user', 'admin')
    tiktok_id = fields.One2many('tiktok.user','admin')