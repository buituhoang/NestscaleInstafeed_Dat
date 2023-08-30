import json

import requests

from odoo import http
from odoo.http import request


class InstagramController(http.Controller):
    @http.route('/instagram/like', type="json", auth='user', cors='*', method=['POST'])
    def get_number_of_like(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])
        like_count = requests.get(f"https://graph.facebook.com/v17.0/{kw['post_id']}?fields=like_count&access_token={shop.facebook_id.user_token}").json()['like_count']
        return json.dumps(like_count)

    @http.route('/instagram/comments', type="json", auth='user', cors='*', method=['POST'])
    def get_number_of_comments(self,**kw):
        shop = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])
        comments_count = requests.get(f"https://graph.facebook.com/v17.0/{kw['post_id']}?fields=comments_count&access_token={shop.facebook_id.user_token}").json()['comments_count']
        return json.dumps(comments_count)

            

