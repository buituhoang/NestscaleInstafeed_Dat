import json

import shopify

from odoo import http
from odoo.http import request


class ShopifyController(http.Controller):
    @http.route('/shopify/products', type="json", auth='user', cors='*', method=['POST'])
    def get_products_shopify(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])
        shop.init_shopify_session()
        if not kw['product_search']:
            products_list_graph_data = json.loads(shopify.GraphQL().execute('''
                    {
                        shop{
                            name
                        }
                        products(first:20){
                            edges{
                                node{
                                    id
                                    title
                                    description
      					            onlineStoreUrl
                                    images(first:1){
                                        edges{
                                            node{
                                                id
                                                originalSrc
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                '''))
        else:
            products_list_graph_data = json.loads(shopify.GraphQL().execute('''
                    {
                        shop{
                            name
                        }
                        products(first:20,query:"title:*'''+kw['product_search']+'''*"){
                            edges{
                                node{
                                    id
                                    title
                                    description
                                    images(first:1){
                                        edges{
                                            node{
                                                id
                                                originalSrc
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                '''))
        products_list_data = []
        for product in products_list_graph_data['data']['products']['edges']:
            products_list_data.append({
                'shopify_shop': products_list_graph_data['data']['shop']['name'],
                'shopify_id':product['node']['id'],
                'title':product['node']['title'],
                'description':product['node']['description'],
                'img':product['node']['images']['edges'][0]['node']['originalSrc']
            })
        return (json.dumps(products_list_data))

    # integrate
    @http.route('/api/integrate/ui', auth='user', cors='*', method=['POST'])
    def integrate_shop_ui(self):
        shops = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])
        shops_data = []
        for shop in shops:
            shops_data.append({
                'name': shop['shop_url']
            })
        return json.dumps(shops_data)

    @http.route('/api/integrate', type='json', auth='user', cors='*', method=['POST'])
    def integrate_shop(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['url'])])
        if shop:
            if not shop['user_id']:
                shop.write(
                    {
                        'user_id': request.env.user.id
                    }
                )

    @http.route('/api/disintegrate', type='json', auth='user', cors='*', method=['POST'])
    def disintegrate_shop(self, **kw):
        shop = request.env['shopify.shop'].sudo().search([('shop_url', '=', kw['url'])])
        if shop:
            if shop['user_id']:
                shop.sudo().write(
                    {
                        'user_id': False
                    }
                )