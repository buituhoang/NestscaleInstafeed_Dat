from odoo import models, fields

class MediaSource(models.Model):
    _name = 'media.source'

    name = fields.Char()
    platform = fields.Char()
    instagram_id = fields.Many2one('instagram.user')
    tiktok_id = fields.Many2one('tiktok.user')
    selected_post_ids = fields.Char()

    on_post_click = fields.Selection([('popup', 'Popup'), ('insta', 'Insta'), ('none', 'None')],default='popup')
    show_like = fields.Boolean()
    show_comment = fields.Boolean()

    feed_id = fields.Many2many('social.feed','feed_media_source_rel')
