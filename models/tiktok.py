from odoo import fields, api, models


class TiktokUser(models.Model):
    _name = "tiktok.user"

    admin = fields.Many2one('res.users')
    open_id = fields.Char()
    union_id = fields.Char()
    profile_img = fields.Char()
    username = fields.Char()
    post_id = fields.One2many('tiktok.post','user_id')

class TiktokPost(models.Model):
    _name = "tiktok.post"

    user_id = fields.Many2one('tiktok.user')
    post_id = fields.Char()
    embed_link = fields.Char()
    share_url = fields.Char()
    cover_img = fields.Char()
    title = fields.Char()
    like_count = fields.Integer()
    comment_count = fields.Integer()
    share_count = fields.Integer()

    hotspot_ids = fields.Many2many('shopify.hotspot', 'tiktok_hotspot_rel')