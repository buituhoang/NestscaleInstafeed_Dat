<template>
  <div class="association content">
    <div class="block">
      <div class="title">E-COMMERCE</div>
      <div class="flex">
        <div class="channel">
          <div class="channel-head">
            <div class="channel-logo"><img src="/instafeed/static/images/full-logo/shopify.png"></div>
            <div class="channel-number-connnection">{{ shopify_account_num }} Connections</div>
          </div>
          <div class="channel-content">
            <div class="description">Manage your Shopify integrations at one place</div>
            <button @click="addShopify">Add shopify</button>
          </div>
        </div>
      </div>
    </div>

    <div class="block">
      <div class="title">SOCIAL CHANNELS</div>
      <div class="flex">
        <div class="channel">
          <div class="channel-head">
            <div class="channel-logo"><img src="/instafeed/static/images/full-logo/tiktok.webp"></div>
            <div class="channel-number-connnection">{{ tiktok_account_num }} Connections</div>
          </div>
          <div class="channel-content">
            <div class="description">Get your TikTok creatives to display on your store</div>
            <button @click="connectTiktok">Connect tiktok</button>
          </div>
        </div>

        <div class="channel">
          <div class="channel-head">
            <div class="channel-logo"><img src="/instafeed/static/images/full-logo/insta.webp"></div>
            <div class="channel-number-connnection">{{ instagram_account_num }} Connections</div>
          </div>
          <div class="channel-content">
            <div class="description">Add stunning Instagram images and videos to your store</div>
            <button @click="connectFacebook">Connect instagram</button>
          </div>
        </div>
      </div>

    </div>

  </div>

</template>

<script>
import axios from "axios";

export default {
  data(){
    return{
      tiktok_account_num:0,
      shopify_account_num:0,
      instagram_account_num:0
    }
  },
  methods:{
    addShopify(){
      this.$router.push({name:'ShopifyAssociation'})
    },
    connectTiktok(){
      window.location.href = '/tiktok/instafeed/auth'
    },
    connectFacebook(){
      window.location.href = 'https://odoo.website/facebook/instafeed/auth'
    },
  },
  mounted(){
    axios.post('/social/num',{
      jsonrpc:2.0,
      params:{}
    }).then(res=> {
      this.tiktok_account_num = JSON.parse(res.data.result)['tiktok_account_num']
      this.shopify_account_num = JSON.parse(res.data.result)['shopify_account_num']
      this.instagram_account_num = JSON.parse(res.data.result)['instagram_account_num']
    })
  }
}
</script>
<style scoped>
.association{
  padding: 20px;
}
.block{
  margin-bottom: 20px;
  padding: 10px;
  background: #eef7ee;
  width: 100%;
  border-radius: 10px;
}

.title{
  padding: 20px 0 0px 25px;
  font-weight: 600;
  font-size: 16px;
  line-height: 24px;
  text-transform: uppercase;
}

.channel{
  background: white;
  margin: 10px 0 10px 20px;
  border-radius: 4px;
  padding: 10px;
  width: 500px;
}

.channel-head{
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.description{
  margin-bottom: 10px;
  color: #777777;
}

.channel-logo img{
  width: 100px;
}

button{
  cursor: pointer;
  background: #202020;
  color: white;
  border: none;
  padding: 10px 15px;
  margin-bottom: 10px;
}
</style>