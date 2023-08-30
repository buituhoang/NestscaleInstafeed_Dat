from odoo import fields, api, models

class ShopifyHotspot(models.Model):
    _name = "shopify.hotspot"

    admin = fields.Many2one('res.user')
    shopify_id = fields.Char()
    tiktok_ids = fields.Many2many('tiktok.post','tiktok_hotspot_rel')
    instagram_ids = fields.Many2many('instagram.post','instagram_hotspot_rel')
    image_url = fields.Char()
    title = fields.Char()