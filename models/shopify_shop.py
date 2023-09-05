import shopify
import time

from odoo import fields, models, api


class ShopifyShop(models.Model):
    _name = 'shopify.shop'

    user_id = fields.Many2one('res.users')
    shop_url = fields.Char()
    shop_name = fields.Char()
    shopify_id = fields.Char()
    currency = fields.Char()
    country = fields.Char()
    email = fields.Char()
    phone = fields.Char()
    token = fields.Char()
    # is_update_script_tag = fields.Boolean()
    is_update_script_tag = fields.Boolean(default=False)
    is_delete = fields.Boolean(default=False)
    # Todo: Thêm trường store domain

    def init_shopify_session(self):
        api_version = self.env['ir.config_parameter'].sudo().get_param('instafeed.shopify_api_version')
        session = shopify.Session(self.shop_url, api_version, self.token)
        shopify.ShopifyResource.activate_session(session)

    def make_webhook(self):
        self.destroy_webhook()

        ngrok_address = self.env["ir.config_parameter"].sudo().get_param("instafeed.ngrok_address")
        shopify.Webhook({
            'topic': "app/uninstalled",
            'address': ngrok_address + f"/webhook/uninstall/{self.id}",
            'format': "json"
        }).save()

    def make_script_tag(self):
        self.destroy_script_tag()
        script_tag = self.env["ir.config_parameter"].sudo().get_param("instafeed.sp_script_tag")
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        shopify.ScriptTag.create({
            "event": "onload",
            "src": base_url+script_tag+'?v=' + str(time.time()),
            "display_scope": "all",
        })
        self.is_update_script_tag = True

    def reset_script_tag(self):
        shops = self.env['shopify.shop'].sudo().search([])
        for shop in shops:
            count = 0
            if shop.is_update_script_tag == False:
                count += 1
                shop.init_shopify_session()
                shop.make_script_tag()
                if count >= 100:
                    break

    def destroy_script_tag(self):
        script_tags = shopify.ScriptTag.find()
        for script_tag in script_tags:
            shopify.ScriptTag.find(script_tag.id).destroy()

    def destroy_webhook(self):
        webhooks = shopify.Webhook.find()
        for webhook in webhooks:
            shopify.Webhook.find(webhook.id).destroy()
