import json

from odoo import fields, api, models


class InstaUser(models.Model):
    _name = "instagram.user"

    instagram_id = fields.Char()
    profile_img = fields.Char()
    username = fields.Char()
    facebook_id = fields.Many2one('facebook.user')
    post_id = fields.One2many('instagram.post','instagram_user_id')

class InstaPost(models.Model):
    _name = 'instagram.post'

    post_id = fields.Char()
    link_to_post = fields.Char()
    media_type = fields.Char()
    media_url = fields.Char()
    thumbnail_url = fields.Char()
    instagram_user_id = fields.Many2one('instagram.user')

    hotspot_ids = fields.Many2many('shopify.hotspot', 'instagram_hotspot_rel')

class InstaFeed(models.Model):
    _name = 'social.feed'

    title = fields.Char()

    feed_id = fields.Char(compute='_hash_feed')
    media_items = fields.Integer(compute='_compute_number_of_media_items')

    post_spacing = fields.Integer(default = 0)
    layout = fields.Selection([('grid-squares','Grid squares'),('grid-tiles','Grid titles')
                                  ,('slider-squares','Slider squares'),('slider-tiles','Slider tiles')],default = 'grid-squares')
    configuration = fields.Selection([('manual','Manual'),('auto','Auto')], default='manual')
    slider_pages = fields.Integer(default = 3)
    number_of_posts = fields.Integer(default = 1)

    admin = fields.Many2one('res.user')
    media_source_ids = fields.Many2many('media.source','feed_media_source_rel')

    def _compute_number_of_media_items(self):
        for rec in self:
            number_of_media_items = 0
            for media_source in rec.media_source_ids:
                number_of_media_items += len(json.loads(media_source['selected_post_ids']))
            rec.media_items = number_of_media_items

    def _hash_feed(self):
        for rec in self:
            rec.feed_id = hash(json.dumps({
                'id':rec.id,
            }))