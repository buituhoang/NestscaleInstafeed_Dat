import json

from odoo import http
from odoo.http import request

class SocialController(http.Controller):
    @http.route('/social/len', type='json', auth='user', cors='*', method=['POST'])
    def social_len(self, **kw):
        return json.dumps({})

    @http.route('/social/info', type='json', auth='user', cors='*', method=['POST'])
    def social(self,*kw):
        social = []
        for facebook in request.env.user.facebook_id:
            insta = facebook.instagram_user_id
            social.append({
                'id':insta.id,
                'platform':'Instagram',
                'username':insta.username,
                'profile_img':insta.profile_img
            })
        for tiktok in request.env.user.tiktok_id:
            social.append({
                'id':tiktok.id,
                'platform':'Tiktok',
                'username':tiktok.username,
                'profile_img':tiktok.profile_img
            })
        return json.dumps(social)

    @http.route('/media_source/list', type='json', auth='user', cors='*', method=['POST'])
    def get_media_source_list(self,**kw):
        media_source_list = []
        for media_source in request.env['media.source'].sudo().search([]):
            source_account = ''
            if media_source['platform'] == 'tiktok':
                source_account = media_source.tiktok_id.username
            elif media_source['platform'] == 'instagram':
                source_account = media_source.instagram_id.username
            media_source_list.append({
                'id':media_source['id'],
                'platform': media_source['platform'],
                'source_name':media_source['name'],
                'source_account':source_account,
                'media_items':len(json.loads(media_source['selected_post_ids'])),
                'last_update':str(media_source['write_date'])
            })
        return json.dumps(media_source_list)

    @http.route('/media_source/create', type='json', auth='user', cors='*', method=['POST'])
    def create_media_source(self,**kw):
        if kw['platform'] == 'tiktok':
            tiktok_account = request.env['tiktok.user'].sudo().browse(kw['id'])
            tiktok_posts = tiktok_account.post_id
            tiktok_posts_ids = []
            for tiktok_post in tiktok_posts:
                tiktok_posts_ids.append(tiktok_post.id)
            request.env['media.source'].sudo().create({
                'name':kw['name'],
                'platform':kw['platform'],
                'tiktok_id': tiktok_account.id,
                'selected_post_ids': json.dumps(tiktok_posts_ids)
            })
        if kw['platform'] == 'instagram':
            instagram_account = request.env['instagram.user'].sudo().browse(kw['id'])
            instagram_posts = instagram_account.post_id
            instagram_posts_ids=[]
            for instagram_post in instagram_posts:
                instagram_posts_ids.append(instagram_post.id)
            request.env['media.source'].sudo().create({
                'name':kw['name'],
                'platform':kw['platform'],
                'instagram_id': instagram_account.id,
                'selected_post_ids': json.dumps(instagram_posts_ids)
            })

    @http.route('/media_source/remove', type='json', auth='user', cors='*', method=['POST'])
    def remove_media_source(self, **kw):
        media_source = request.env['media.source'].sudo().browse(kw['media_source_id'])
        media_source.sudo().unlink()

    @http.route('/media_source/posts', type='json', auth='user', cors='*', method=['POST'])
    def media_source_products(self, **kw):
        media_source = request.env['media.source'].sudo().browse(kw['media_source_id'])
        selected_post = json.loads(media_source['selected_post_ids'])
        post_list= {
            'list':[],
            'platform':'',
            'setting':{
                'on_post_click':media_source['on_post_click'],
                'show_like':media_source['show_like'],
                'show_comment':media_source['show_comment']
            }
        }
        if media_source.platform == 'tiktok':
            for post in media_source.tiktok_id.post_id:
                is_showed = False
                if post.id in selected_post:
                    is_showed = True
                post_list['list'].append({
                    'post_id': post.id,
                    'media_url': post.embed_link,
                    'media_type': 'VIDEO',
                    'thumbnail_url': post.cover_img,
                    'link_to_post':post.share_url,
                    'is_showed':is_showed
                })
            post_list['platform'] = 'tiktok'
        if media_source.platform == 'instagram':
            for post in media_source.instagram_id.post_id:
                is_showed = False
                if post.id in selected_post:
                    is_showed = True
                post_list['list'].append({
                    'post_id': post.id,
                    'media_url':post.media_url,
                    'media_type': post.media_type,
                    'thumbnail_url':post.thumbnail_url,
                    'link_to_post':post.link_to_post,
                    'is_showed':is_showed
                })
            post_list['platform'] = 'instagram'

        return json.dumps(post_list)

    @http.route('/media_source/posts/hide', type='json', auth='user', cors='*', method=['POST'])
    def hide_posts_media_source(self, **kw):
        media_source = request.env['media.source'].sudo().browse(kw['media_source_id'])
        selected_post_ids = json.loads(media_source['selected_post_ids'])
        for post_id in kw['selected_post']:
            if post_id in selected_post_ids:
                selected_post_ids.remove(post_id)
        media_source.write({
            'selected_post_ids':selected_post_ids
        })


    @http.route('/media_source/posts/show', type='json', auth='user', cors='*', method=['POST'])
    def show_posts_media_source(self, **kw):
        media_source = request.env['media.source'].sudo().browse(kw['media_source_id'])
        selected_post_ids = json.loads(media_source['selected_post_ids'])
        for post_id in kw['selected_post']:
            if post_id not in selected_post_ids:
                selected_post_ids.append(post_id)
        media_source.write({
            'selected_post_ids': selected_post_ids
        })

    @http.route('/media_source/hotspot', type='json', auth='user', cors='*', method=['POST'])
    def make_hotspot(self,**kw):
        product = request.env['shopify.hotspot'].sudo().search([('shopify_id','=',kw['product_choosen'])])
        if not product:
            product = request.env['shopify.hotspot'].sudo().create({
                'shopify_id':kw['product_choosen'],
                'title':kw['product_title'],
                'image_url':kw['product_img']
            })
        else:
            product.write({
                'title': kw['product_title'],
                'image_url': kw['product_img']
            })
        if kw['platform'] == 'tiktok':
            post = request.env['tiktok.post'].sudo().search([('id','=',kw['post_id'])])
            post.write({
                'hotspot_ids': [(4,product.id)]
            })

        if kw['platform'] == 'instagram':
            post = request.env['instagram.post'].sudo().search([('id','=',kw['post_id'])])
            post.write({
                'hotspot_ids': [(4, product.id)]
            })

    @http.route('/media_source/delete_hotspot', type='json', auth='user', cors='*', method=['POST'])
    def remove_hotspot(self,**kw):
        product = request.env['shopify.hotspot'].sudo().search([('shopify_id','=',kw['product_choosen'])])
        if not product:
            product = request.env['shopify.hotspot'].sudo().create({
                'shopify_id':kw['product_choosen'],
                'title':kw['product_title'],
                'image_url':kw['product_img']
            })
        else:
            product.write({
                'title': kw['product_title'],
                'image_url': kw['product_img']
            })
        if kw['platform'] == 'tiktok':
            post = request.env['tiktok.post'].sudo().search([('id','=',kw['post_id'])])
            post.write({
                'hotspot_ids': [(2,product.id)]
            })

        if kw['platform'] == 'instagram':
            post = request.env['instagram.post'].sudo().search([('id','=',kw['post_id'])])
            post.write({
                'hotspot_ids': [(2, product.id)]
            })

    @http.route('/media_source/hotspot/products_choosen', type='json', auth='user', cors='*', method=['POST'])
    def get_product_choosen(self,**kw):
        product_choosen = []
        if kw['platform'] == 'tiktok':
            post = request.env['tiktok.post'].sudo().search([('id','=',kw['post_id'])])
            for hotspot in post.hotspot_ids:
                product_choosen.append(hotspot.shopify_id)
        if kw['platform'] == 'instagram':
            post = request.env['instagram.post'].sudo().search([('id','=',kw['post_id'])])
            for hotspot in post.hotspot_ids:
                product_choosen.append(hotspot.shopify_id)

        return json.dumps(product_choosen)


    @http.route('/media_source/change/<string:attribute>', type='json', auth='user', cors='*', method=['POST'])
    def change_attribute_media_source(self, **kw):
        media_source = request.env['media.source'].sudo().browse(kw['media_source_id'])
        media_source.write({
            kw['attribute']:kw[kw['attribute']]
        })

    @http.route('/feed/create', type='json', auth='user', cors='*', method=['POST'])
    def create_feed(self, **kw):
        feed_created = request.env['social.feed'].sudo().create({
            'title':kw['feed_name'],
            'media_source_ids':[(6,0,kw['media_source_ids'])]
        })
        return json.dumps({
            'feed_id':feed_created.id
        })

    @http.route('/feed/list', type='json', auth='user', cors='*', method=['POST'])
    def get_feed_list(self):
        feed_list = []
        for feed in request.env['social.feed'].sudo().search([]):
            feed_list.append({
                'id':feed['id'],
                'feed_name':feed.title,
                'feed_id':feed['feed_id'],
                'media_items':feed['media_items'],
                'media_source':len(feed['media_source_ids']),
                'last_update':str(feed['write_date']),
            })
        return json.dumps(feed_list)

    @http.route('/feed/remove', type='json', auth='user', cors='*', method=['POST'])
    def remove_feed(self,**kw):
        feed = request.env['social.feed'].sudo().browse(kw['feed_id'])
        feed.unlink()

    @http.route('/feed/posts', type="json", auth='none', crsf=False, cors='*', method=['POST'])
    def get_feed_posts(self, **kw):
        feed_posts = {
            'posts':[],
            'setting':{}
        }
        if 'hash_feed_id' in kw:
            feed = request.env['social.feed'].sudo().search([('feed_id', '=', kw['hash_feed_id'])], limit=1)
        else:
            feed = request.env['social.feed'].sudo().search([('id','=',kw['feed_id'])],limit=1)
        media_sources = feed['media_source_ids']
        for media_source in media_sources:
            if media_source.platform == 'tiktok':
                for post in media_source.tiktok_id.post_id:
                    if post.id in json.loads(media_source.selected_post_ids):
                        feed_posts['posts'].append({
                            'post_id': post.id,
                            'media_url': post.embed_link,
                            'media_type': 'VIDEO',
                            'thumbnail_url': post.cover_img,
                            'link_to_post': post.share_url,
                            'is_showed':True,
                            'on_post_click': media_source['on_post_click'],
                            'show_like': media_source['show_like'],
                            'show_comment': media_source['show_comment'],
                            'platform':media_source['platform']
                        })
            if media_source.platform == 'instagram':
                for post in media_source.instagram_id.post_id:
                    if post.id in json.loads(media_source.selected_post_ids):
                        feed_posts['posts'].append({
                            'post_id': post.id,
                            'media_url': post.media_url,
                            'media_type': post.media_type,
                            'thumbnail_url': post.thumbnail_url,
                            'link_to_post': post.link_to_post,
                            'is_showed':True,
                            'on_post_click': media_source['on_post_click'],
                            'show_like': media_source['show_like'],
                            'show_comment': media_source['show_comment'],
                            'platform':media_source['platform']
                        })

        feed_posts['setting']['title'] = feed.title
        feed_posts['setting']['post_spacing'] = feed.post_spacing
        feed_posts['setting']['layout'] = feed.layout
        feed_posts['setting']['configuration'] = feed.configuration
        feed_posts['setting']['number_of_posts'] = feed.number_of_posts
        feed_posts['setting']['slider_pages'] = feed.slider_pages
        return json.dumps(feed_posts)

    @http.route('/feed/change/<string:attribute>', type='json', auth='user', cors='*', method=['POST'])
    def change_attribute_feed(self, **kw):
        feed = request.env['social.feed'].sudo().search([('id','=',kw['feed_id'])],limit=1)
        feed.write({
            kw['attribute']: kw[kw['attribute']]
        })

    @http.route('/social/num', type='json', auth='user', cors='*', method=['POST'])
    def get_social_num(self):
        tiktok_account_num  = request.env['tiktok.user'].sudo().search([('admin','=',request.env.user.id)])
        instagram_account_num  = request.env['facebook.user'].sudo().search([('admin','=',request.env.user.id)])
        shopify_account_num  = request.env['shopify.shop'].sudo().search([('user_id','=',request.env.user.id)])

        return json.dumps({
            'tiktok_account_num':len(tiktok_account_num),
            'instagram_account_num':len(instagram_account_num),
            'shopify_account_num':len(shopify_account_num),
        })