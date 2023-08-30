from odoo import models,fields
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    instafeed_ngrok_address = fields.Char('NGROK address', config_parameter='instafeed.ngrok_address')

    instafeed_shopify_api_version = fields.Char('API Version', config_parameter='instafeed.shopify_api_version')
    instafeed_shopify_key = fields.Char('Client Key', config_parameter='instafeed.shopify_key')
    instafeed_shopify_secret = fields.Char('Secret Key', config_parameter='instafeed.shopify_secret')
    instafeed_sp_script_tag = fields.Char('Script Tag',config_parameter='instafeed.sp_script_tag')

    instafeed_facebook_client_id = fields.Char('Facebook app id', config_parameter='instafeed.facebook_client_id')
    instafeed_facebook_redirect_uri = fields.Char('Facebook redirect URI', config_parameter='instafeed.facebook_redirect_uri')
    instafeed_facebook_secret = fields.Char('Facebook client secret', config_parameter="instafeed.facebook_secret")

    instafeed_tiktok_app_id = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_app_id')
    instafeed_tiktok_client_key = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_client_key')
    instafeed_tiktok_secret_key = fields.Char('Facebook app id', config_parameter='instafeed.tiktok_secret_key')

    def add_script_tag_to_shop_shopify_shop(self):
        shops = self.env['shopify.shop'].sudo().search([])
        for shop in shops:
            shop.init_shopify_session()
            shop.is_update_script_tag = False