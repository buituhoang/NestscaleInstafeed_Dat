from odoo import http
import json
import shopify
from odoo.http import request


class WebhookController(http.Controller):
    @http.route('/webhook/orders_create/<int:id>',type='json', auth="public")
    def webhook_check(self,**kw):
        print(kw)
        return {}
    @http.route('/webhook/orders_update/<int:id>',type='json', auth="public")
    def webhook_check(self,**kw):
        print(kw)
        return {}
    @http.route('/webhook/products_create/<int:id>',type='json', auth="public")
    def webhook_check(self,**kw):
        print(request.jsonrequest)
        return {}

    @http.route('/webhook/products_update/<int:id>',type='json', auth="public")
    def webhook_check(self,**kw):
        print(request.jsonrequest)
        return {}

    @http.route('/webhook/uninstall/<int:id>',type='json', auth="public")
    def webhook_check(self,id,**kw):
        shop = request.env['shopify.shop'].browse(id)
        shop.init_shopify_session()
        shop.is_delete = True
        shop.destroy_scrip_tag()
        shop.destroy_webhook()
        return {}

