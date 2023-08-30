import binascii
import os
import traceback

import shopify
import werkzeug

import odoo
from odoo import http
import json
from odoo.addons.portal.controllers.portal import CustomerPortal

from odoo.http import request, _logger


class CustomerPortal(CustomerPortal):
    @odoo.http.route()
    def home(self):
        return werkzeug.utils.redirect('/apps/instafeed')


class AuthShopifyController(http.Controller):
    @http.route('/shopify/instafeed/auth', auth='public')
    def shopify_auth2(self, **kw):
        if 'shop' in kw:
            api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
            shopify_key = request.env['ir.config_parameter'].sudo().get_param('shopify_key')
            shopify_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_secret')

            shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)

            shop_url = kw['shop']
            state = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
            redirect_uri = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + "/shopify/instafeed/finalize"
            scopes = [
                "read_products",
                "read_orders",
                "write_orders",
                'read_script_tags',
                'write_script_tags',
                'read_themes'
            ]

            newSession = shopify.Session(shop_url, api_version)
            auth_url = newSession.create_permission_url(scopes, redirect_uri, state)

            return werkzeug.utils.redirect(auth_url)
        else:
            raise Exception('Missing shop url parameter')

    @http.route('/shopify/instafeed/finalize', autgeth="public", type="http", cors="*")
    def shopify_callback(self, **kw):
        if 'shop' not in request.params:
            raise Exception('Missing shop url parameter')

        api_version = request.env['ir.config_parameter'].sudo().get_param('shopify_api_version')
        shopify_key = request.env['ir.config_parameter'].sudo().get_param('shopify_key')
        shopify_secret = request.env['ir.config_parameter'].sudo().get_param('shopify_secret')

        shop_url = kw['shop']

        try:
            shopify.Session.setup(api_key=shopify_key, secret=shopify_secret)
            shopify_session = shopify.Session(shop_url, api_version)
            access_token = shopify_session.request_token(kw)
            shopify.ShopifyResource.activate_session(shopify_session)

            if access_token:
                shopify_shop = shopify.Shop.current()  # Get the current shop

                shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['shop'])])
                if not shop:
                    self.make_new_shop(shopify_shop, access_token)
                else:
                    self.upgrade_shop_info(shop, shopify_shop, access_token)

                shop.make_webhook()
                shop.make_script_tag()

                return werkzeug.utils.redirect('/apps/instafeed')
        except Exception as e:
            _logger.error(traceback.format_exc())
            return e.__class__.__name__ + ': ' + str(e) + ' .Please try again!'

    def make_new_shop(self, shopify_shop, access_token):
        if request.env.user:
             created_shop = request.env['shopify.shop'].sudo().create({
                'shopify_id': shopify_shop.id,
                'shop_url': shopify_shop.domain,
                'shop_name': shopify_shop.name,
                'currency': shopify_shop.currency,
                'country': shopify_shop.country,
                'phone': shopify_shop.phone,
                'email': shopify_shop.email,
                'token': access_token,
                'user_id': request.env.user.id
             })
             request.env.user.shop_id = created_shop.id
        else:
            request.env['shopify.shop'].sudo().create({
                'shopify_id': shopify_shop.id,
                'shop_url': shopify_shop.domain,
                'shop_name': shopify_shop.name,
                'currency': shopify_shop.currency,
                'country': shopify_shop.country,
                'phone': shopify_shop.phone,
                'email': shopify_shop.email,
                'token': access_token
            })

    def upgrade_shop_info(self, shop, shopify_shop, access_token):
        if shop.user_id:
            shop.sudo().write({
                'shopify_id': shopify_shop.id,
                'shop_url': shopify_shop.domain,
                'shop_name': shopify_shop.name,
                'currency': shopify_shop.currency,
                'country': shopify_shop.country,
                'phone': shopify_shop.phone,
                'email': shopify_shop.email,
                'token': access_token,
            })
        else:
            if request.env.user:
                created_shop = shop.sudo().write({
                    'user_id': request.env.user.id,
                    'shopify_id': shopify_shop.id,
                    'shop_url': shopify_shop.domain,
                    'shop_name': shopify_shop.name,
                    'currency': shopify_shop.currency,
                    'country': shopify_shop.country,
                    'phone': shopify_shop.phone,
                    'email': shopify_shop.email,
                    'token': access_token,
                })
                request.env.user.shop_id = created_shop.id
            else:
                shop.sudo().write({
                    'shopify_id': shopify_shop.id,
                    'shop_url': shopify_shop.domain,
                    'shop_name': shopify_shop.name,
                    'currency': shopify_shop.currency,
                    'country': shopify_shop.country,
                    'phone': shopify_shop.phone,
                    'email': shopify_shop.email,
                    'token': access_token,
                })

    @http.route('/apps/instafeed', auth='user')
    def main(self, **kw):
        return self.render_ui()

    @http.route('/apps/instafeed/<string:components>', auth="user", type="http", cors="*")
    def app_shopify_xero_branch(self):
        return self.render_ui()

    @http.route('/apps/instafeed/<string:components>/<string:components2>', auth="user", type="http", cors="*")
    def app_shopify_xero_branch2(self):
        return self.render_ui()

    def render_ui(self):
        value = {
            'user_name': request.env.user.name
        }
        return request.render('instafeed.app-test', {'app_setting': json.dumps(value)})
