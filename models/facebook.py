from odoo import fields, api, models


class FacebookUser(models.Model):
    _name = "facebook.user"

    admin = fields.Many2one('res.users')
    user_token = fields.Char()
    app_token = fields.Char()
    user_id = fields.Char()
    code = fields.Char()
    instagram_user_id = fields.Many2one('instagram.user')


