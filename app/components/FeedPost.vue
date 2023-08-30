<template>
  <div class="feed-post" @mouseover="post_hover = true" @mouseleave="post_hover = false" :style="{backgroundImage:'url('+get_background_url+')'}">
    <div v-if="click_type == 'popup' && post.is_showed" @click="post_modal=true" class="feed-modal" :class="{'display-none':!post_hover}">
      <i class="fa-solid fa-camera"></i>
      <Modal v-model:visible="post_modal"
             style="width: 70%"
             :footer="null">
        <div class="flex">
          <div class="modal-img" v-if="platform=='instagram'">
            <img v-if="post.media_type == 'IMAGE'" :src="post.media_url">
            <video v-if="post.media_type == 'VIDEO'" controls>
              <source :src="post.media_url" type="video/mp4">
            </video>
          </div>
          <div v-else>
            <iframe :src="post.media_url" width="800px" height="700px">

            </iframe>
          </div>
          <div class="modal-product">
            <div class="modal-header">
              <img v-if="platform == 'instagram'" src="/instafeed/static/images/logo/ins.png">
              <img v-if="platform == 'tiktok'" src="/instafeed/static/images/logo/tiktok.png">
              <span>{{insta_name}}</span>
            </div>

            <div class="interaction">
              <span v-if="number_of_likes!=null" :class="{pink_heart:number_of_likes>0}"><i :class="{pink_heart:number_of_likes>0}" class="fa-regular fa-heart"></i> {{number_of_likes}}</span>
              <span v-if="number_of_comments!=null" :class="{green_comments:number_of_comments>0}"><i :class="{green_comments:number_of_comments>0}" class="fa-regular fa-comment"></i> {{number_of_comments}}</span>
            </div>

            <div class="product-list">
              <button v-if="customize_hotspot" @click="product_modal=true">Tag products</button>
              <div v-for="product in products_list" class="product-row">
                <div v-if="this.products_choosen.includes(product.shopify_id)" class="flex">
                  <span v-if="customize_hotspot" @click="choose_product(product.shopify_id,product.img,product.title)" class="remove-product-choosen">x</span>
                  <div @click="go_to_product_shopify(product.shopify_shop,product.title)" class="flex pointer">
                      <img :src="product.img">
                      {{product.title}}
                  </div>
                </div>
              </div>
            </div>
          </div>
          <Modal v-model:visible="product_modal" style="borderRadius:4px;width:40%" title="Add prodduct" :footer="null">
            <input v-model="product_search" type="text" class="product-search" placeholder="Search products">
            <div v-for="product in products_list" class="product-row">
              <input @click="choose_product(product.shopify_id,product.img,product.title)"
                     type="checkbox" :checked="this.products_choosen.includes(product.shopify_id)">
                <img :src="product.img">
                {{product.title}}
            </div>
          </Modal>
        </div>
      </Modal>
    </div>
    <div v-else-if="click_type == 'insta' && post.is_showed" @click="go_to_insta" class="feed-modal" :class="{'display-none':!post_hover}">
      <i class="fa-solid fa-camera"></i>
    </div>
    <div v-if="!post.is_showed" class="feed-modal">
      <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" clip-rule="evenodd" d="M32 40C36.42 40 40 36.416 40 32C40 31.288 39.88 30.608 39.704 29.952L62.828 6.82802C64.392 5.26402 64.392 2.73602 62.828 1.17202C61.264 -0.391977 58.736 -0.391977 57.172 1.17202L46.732 11.612C42.664 9.46002 37.796 8.00002 32 8.00002C9.55202 8.00002 0.652023 29.596 0.284023 30.512C-0.0919765 31.468 -0.0919765 32.532 0.284023 33.488C0.500023 34.02 3.62402 41.532 10.612 47.732L1.17202 57.172C-0.391977 58.736 -0.391977 61.264 1.17202 62.828C1.95202 63.608 2.97602 64 4.00002 64C5.02402 64 6.04802 63.608 6.82802 62.828L29.952 39.704C30.608 39.876 31.288 40 32 40ZM16 32C16 23.164 23.164 16 32 16C34.968 16 37.728 16.832 40.1 18.244L34.048 24.296C33.392 24.124 32.716 24 32 24C27.584 24 24 27.584 24 32C24 32.712 24.124 33.388 24.296 34.044L18.244 40.1C16.836 37.724 16 34.964 16 32ZM56.578 19.422L47.57 28.43C47.83 29.582 47.998 30.77 47.998 32.002C47.998 40.838 40.838 48.002 31.998 48.002C30.77 48.002 29.586 47.834 28.434 47.57L21.706 54.294C24.774 55.338 28.174 56.002 31.998 56.002C54.45 56.002 63.346 34.406 63.714 33.486C64.094 32.53 64.094 31.47 63.714 30.514C63.538 30.07 61.33 24.766 56.578 19.422Z" fill="#1A1C1D"></path></svg>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {Modal} from "ant-design-vue";
import {debounce} from "lodash";
export default {
  components:{Modal},
  props:['post','click_type','show_like','show_comment','platform','customize_hotspot'],
  data(){
    return{
      post_hover:false,
      post_modal:false,
      product_modal:false,
      insta_name:window.app_settings.insta_name,
      products_list:[],
      product_search:'',
      products_choosen:[],
      number_of_likes:null,
      number_of_comments:null
    }
  },
  methods:{
    search_products:debounce(function () {
      let self = this
      axios.post('/shopify/products',{
        jsonrpc:2.0,
        params:{
          product_search:self.product_search
        }
      }).then(res => self.products_list = JSON.parse(res.data.result))
    },500),
    choose_product(id,product_img,product_title){
      if(!this.products_choosen.includes(id)){
        axios.post('/media_source/hotspot',{
          jsonrpc:2.0,
          params:{
            post_id:this.post.post_id,
            platform:this.platform,
            product_choosen: id,
            product_img: product_img,
            product_title:product_title
          }
        })
        this.products_choosen.push(id)
        this.$store.state.posts[this.post.post_id] = this.products_choosen
      }else{
        axios.post('/media_source/delete_hotspot',{
          jsonrpc:2.0,
          params:{
            post_id:this.post.post_id,
            platform:this.platform,
            product_choosen: id,
            product_img: product_img,
            product_title:product_title
          }
        })
        this.products_choosen.splice(this.products_choosen.indexOf(id),1)
        this.$store.state.posts[this.post.post_id] = this.products_choosen
      }
    },
    go_to_insta(){
      window.location.href = this.post['link_to_post']
    },
    watch_like(){
      axios.post('/instagram/like',{
        jsonrpc:2.0,
        params:{
          post_id:this.post.post_id
        }
      }).then(res => this.number_of_likes = JSON.parse(res.data.result))
    },
    watch_comments(){
      axios.post('/instagram/comments',{
        jsonrpc:2.0,
        params:{
          post_id:this.post.post_id
        }
      }).then(res => this.number_of_comments = JSON.parse(res.data.result))
    },
    go_to_product_shopify(shopify_name,product_title){
      let url = `https://${shopify_name.toLowerCase().replace(/ /g,'-')}.myshopify.com/products/${product_title}`
      window.location.href = url
    },
  },
  computed:{
    get_background_url(){
      if (this.post.media_type == 'VIDEO'){
        return this.post.thumbnail_url
      }
      return this.post.media_url
    }
  },
  watch:{
    product_search(newProductSearch,oldProductSearch){
      this.search_products()
    },
    show_like(newValue,oldValue){
      if (newValue === true){
        this.watch_like()
      }else{
        this.number_of_likes = null
      }
    },
    show_comment(newValue,oldValue){
      if (newValue === true){
        this.watch_comments()
      }else{
        this.number_of_comments = null
      }
    }
  },
  mounted() {
    axios.post('/shopify/products',{
        jsonrpc:2.0,
        params:{
          product_search:this.product_search
        }
      }).then(res => this.products_list = JSON.parse(res.data.result))
    if(this.show_like === true){
      this.watch_like()
    }
    if(this.show_comment === true){
      this.watch_comments()
    }
    axios.post('/media_source/hotspot/products_choosen',{
        jsonrpc:2.0,
        params:{
          post_id:this.post.post_id,
          platform:this.platform,
        }
      }).then(res => this.products_choosen = JSON.parse(res.data.result))
  }
}
</script>

<style scoped>

  .feed-post{
    width: 100%;
    height: 100%;
    background-size: cover;
    background-position:center;
  }

  .feed-modal{
    position: absolute;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.25);
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
  }

  .feed-modal i{
    color: white;
    font-size: 20px;
  }

  img{
    width: 100%;
  }

  .modal-img{
    width: 60%;
  }

  .modal-product{
    width: 40%;
    padding: 10px;
  }

  .modal-header{
    width: 100%;
    padding: 20px;
    display: flex;
    align-items: center;
    border-bottom: 1px solid #d5d5d5;
  }

  .modal-header img{
    width: 30px;
    height: 30px;
  }

  .modal-header span{
    font-size: 18px;
    font-weight: 450;
    margin-left: 20px;
  }

  .product-list button{
    margin: 30px auto;
    display: block;
    background: #41c741;
    color: white;
    font-size: 16px;
    font-weight: 500;
    padding: 5px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .product-row{
    padding: 5px 20px;
    display: flex;
    align-items: center;
  }

  .product-row input[type='checkbox']{

  }

  .product-row img{
    width: 50px;
    height: 50px;
    margin:0 30px;
  }

  .product-search{
    margin: 10px auto;
    width: 90%;
    display: block;
  }

  .remove-product-choosen{
    color:red;
    margin-left: 20px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
  }

  .interaction{
    padding: 10px;
  }

  .interaction span{
    margin-right: 20px;
  }

  .pink_heart{
    color:pink;
  }

  .green_comments{
    color: #39a839;
  }
</style>
<style src="../css/custom_modal.css"></style>