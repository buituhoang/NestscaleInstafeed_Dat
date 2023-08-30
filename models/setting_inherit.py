from odoo import models,fields
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ngrok_address = fields.Char('NGROK address', config_parameter='ngrok_address')

    shopify_api_version = fields.Char('API Version', config_parameter='shopify_api_version')
    shopify_key = fields.Char('Client Key', config_parameter='shopify_key')
    shopify_secret = fields.Char('Secret Key', config_parameter='shopify_secret')
    sp_script_tag = fields.Char('Script Tag',config_parameter='sp_script_tag')

    facebook_client_id = fields.Char('Facebook app id', config_parameter='instafeed.facebook_client_id')
    facebook_redirect_uri = fields.Char('Facebook redirect URI', config_parameter='instafeed.facebook_redirect_uri')
    facebook_secret = fields.Char('Facebook client secret', config_parameter="instafeed.facebook_secret")

    tiktok_app_id = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_app_id')
    tiktok_client_key = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_client_key')
    tiktok_secret_key = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_secret_key')

    def add_script_tag_to_shop_shopify_shop(self):
        shops = self.env['shopify.shop'].sudo().search([])
        for shop in shops:
            shop.init_shopify_session()
            shop.is_update_script_tag = False