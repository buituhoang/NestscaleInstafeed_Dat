import requests
import werkzeug

from odoo import http
from odoo.http import request

SCOPE = 'pages_show_list,instagram_basic,pages_manage_engagement,business_management,pages_messaging'

class FacebookController(http.Controller):
    @http.route('/facebook/instafeed/auth', auth='public')
    def meta_auth(self):
        facebook_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_client_id')
        facebook_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_redirect_uri')
        facebook_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_secret')

        return werkzeug.utils.redirect(f'https://www.facebook.com/v17.0/dialog/oauth?client_id={facebook_client_id}&redirect_uri={facebook_redirect_uri}&scope={SCOPE}')


    @http.route('/facebook/instafeed/oauth', auth='public')
    def meta_callback(self,**kw):
        facebook_client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_client_id')
        facebook_redirect_uri = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_redirect_uri')
        facebook_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.facebook_secret')

        get_token_uri = ('https://graph.facebook.com/v17.0/oauth/access_token')
        get_token_param = {
            'redirect_uri' :facebook_redirect_uri,
            'client_id': facebook_client_id,
            'client_secret': facebook_secret,
            'code' : kw['code']
        }

        facebook_token_data = requests.post(get_token_uri, get_token_param)
        facebook_token = facebook_token_data.json()['access_token']

        app_access_token_data = requests.get(f'https://graph.facebook.com/oauth/access_token?client_id={facebook_client_id}&client_secret={facebook_secret}&grant_type=client_credentials')
        app_access_token = app_access_token_data.json()['access_token']

        facebook_user_data = requests.get(f'https://graph.facebook.com/debug_token?input_token={facebook_token}&access_token={app_access_token}')
        facebook_user = facebook_user_data.json()['data']

        current_facebook_user = request.env['facebook.user'].sudo().search([('user_id','=',facebook_user['user_id'])])
        if not current_facebook_user:
            facebook_new = request.env['facebook.user'].sudo().create({
                'admin':request.env.user.id,
                'user_token':facebook_token,
                'app_token': app_access_token,
                'user_id': facebook_user['user_id'],
                'code': kw['code'],
            })
            facebook_new_id = facebook_new.id
        else:
            current_facebook_user.sudo().write({
                'admin': request.env.user.id,
                'user_token': facebook_token,
                'app_token': app_access_token,
                'code': kw['code'],
            })
            facebook_new_id = current_facebook_user.id

        page_data = requests.get(f"https://graph.facebook.com/me/accounts?access_token={facebook_token}").json()
        page_data_id = page_data['data'][0]['id']

        get_id_insta_data = requests.get(f"https://graph.facebook.com/v17.0/{page_data_id}?fields=instagram_business_account&access_token={facebook_token}").json()
        insta_id = get_id_insta_data["instagram_business_account"]['id']

        user_insta_data =  requests.get(f"https://graph.facebook.com/v17.0/{insta_id}?fields=name,profile_picture_url&access_token={facebook_token}").json()

        insta_user = request.env['instagram.user'].sudo().search([('instagram_id','=',insta_id)],limit=1)
        if not insta_user:
            insta_user = request.env['instagram.user'].sudo().create({
                'instagram_id':insta_id,
                'facebook_id':facebook_new_id,
                'profile_img':user_insta_data['profile_picture_url'],
                'username':user_insta_data['name']
            })

            current_facebook_user.sudo().write({
                'instagram_user_id':insta_user.id
            })
        else:
            insta_user.sudo().write({
                'facebook_id': facebook_new_id,
                'profile_img': user_insta_data['profile_picture_url'],
                'username': user_insta_data['name']
            })

            current_facebook_user.sudo().write({
                'instagram_user_id': insta_user.id
            })

        insta_data_fields = 'media_url,permalink,media_type,thumbnail_url'
        insta_data = requests.get(f"https://graph.facebook.com/v17.0/{insta_id}/media?fields={insta_data_fields}&access_token={facebook_token}").json()
        for post in insta_data['data']:
            post_search = request.env['instagram.post'].sudo().search([('post_id','=',post['id'])],limit=1)
            if not post_search:
                post_search = request.env['instagram.post'].sudo().create({
                    'post_id':post['id'],
                    'instagram_user_id':insta_user.id,
                    'media_url':post['media_url'],
                    'link_to_post': post['permalink'],
                    'media_type':post['media_type']
                })
            else:
                post_search.sudo().write({
                    'instagram_user_id': insta_user.id,
                    'media_url': post['media_url'],
                    'link_to_post': post['permalink'],
                    'media_type':post['media_type'],
                })

            if post['media_type'] == 'VIDEO':
                post_search.write({
                    'thumbnail_url': post['thumbnail_url']
                })

        return werkzeug.utils.redirect('https://odoo.website/apps/instafeed')