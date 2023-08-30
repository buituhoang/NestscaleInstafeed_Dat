<template>
    <div class="integrations content">
        <router-link :to="{name:'Association'}" class="back back-association">
          	&lt;
        </router-link>
        <div class="main">
            <div class="welcome">
                <i class="fa-solid fa-cart-shopping"></i>
                <span>
                    Let integrate your shop with us!
                </span>
            </div>
            <div>
              <h2>Connect to Shopify</h2>
              <p>Your store name is in the form: https://<strong>mystore</strong>, so you would input "mystore" to connect.</p>
            </div>
            <div class="input">
                <input v-model="url" type="text" placeholder="Want manage you shopify app easily? Paste your store here!">
                <div @click="integrate" class="integrate-btn">Integrate</div>
            </div>
            <div v-for="shop in shops" class="integrated-shop">
                <div  class="integrated-shop-name">
                    {{shop.name}} <i @click="refreshWebhook(shop.name)" class="fa-solid fa-arrows-rotate cursor-pointer"></i> <i @click="refreshScriptTag(shop.name)" class="fa-regular fa-flag cursor-pointer"></i>
                </div>
                <div @click="disintegrate(shop.name)" class="disintegrate-btn">
                    X
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";
import { notification } from 'ant-design-vue';
export default {
    data(){
      return{
          url:'',
          shops: []
      }
    },
    methods:{
        integrate(){
            axios.post('/api/integrate',{
                jsonrpc:2.0,
                params:{
                    url:this.url
                }
            })
            .then(async ()=>{
                await this.shops.push({'name':this.url})
                await console.log(this.shops)
                this.url = ''
            })
            .catch(err => {
                console.log(err)
            })
        },
        disintegrate(shop){
            axios.post('/api/disintegrate',{
                jsonrpc:2.0,
                params:{
                    url: shop
                }
            })
            .then((res)=>{
                this.shops.splice(this.shops.indexOf(shop),1)
            })
            .catch(err => {
                console.log(err)
            })
        },
        refreshWebhook(shop){
          axios.post('/api/refresh_webhook',{
                jsonrpc:2.0,
                params:{
                  url: shop
                }
            })
            .then(() => {
              notification.open({
                message: 'Refresh webhook',
                description:
                  'Your webhook has refreshed successfully',
                onClick: () => {
                  console.log('Notification Clicked!');
                },
              });
            })
            .catch(err => {
                console.log(err)
            })
        },
        refreshScriptTag(shop){
          axios.post('/api/refresh_script_tag',{
                jsonrpc:2.0,
                params:{
                  url: shop
                }
            })
            .then(() => {
              notification.open({
                message: 'Refresh script tag',
                description:
                  'Your script tag has refreshed successfully',
                onClick: () => {
                  console.log('Notification Clicked!');
                },
              });
            })
            .catch(err => {
                console.log(err)
            })
        }
    },
    mounted() {
        axios.get('https://odoo.website/api/integrate/ui',)
            .then(response => this.shops = response.data)
            .catch(err => console.log(err))
    }
}
</script>

<style scoped>
    .back-association{
        position: absolute;
        top: 70px;
        left: 321px;
    }
    .fa-cart-shopping{
        font-size: 150px;
        color: #c1c1c1;
    }
    .integrations{
        justify-content: center;
        display: flex;
    }

    .main{
        width: 60%;
    }

    .welcome{
        margin: 140px 0 50px;
        padding: 10px 50px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .welcome span{
        letter-spacing: -1px;
        font-style: italic;
        padding-left: 40px;
        font-weight: 200;
        font-size: 2.2em;
    }

    h2{
      font-size: 28px;
    }

    .input{
        position: relative;
    }

    .integrations input{
        font-size: 20px;
        border-color: #00000038;
        padding: 10px 124px 10px 40px;
        border-radius: 32px;
        width: 100%;
    }

    .integrations input:focus-visible{
        outline: none;
    }

    .integrate-btn{
        font-size: 16px;
        padding: 11px 20px;
        position: absolute;
        top: 4px;
        right: 4px;
        border-radius: 30px;
        background: #815656;
        font-weight: 600;
        color: white;
        cursor: pointer;
    }

    .integrated-shop{
        display: flex;
        margin-top: 20px;
    }

    .integrated-shop-name{
        border-radius: 26px;
        padding: 10px;
        background: green;
        color: white;
        width: fit-content;
    }
    .integrated-shop-name i{
      margin-left: 10px;
    }

    .disintegrate-btn{
        margin-top: 10px;
        font-weight: 900;
        margin-left: 10px;
        font-size: larger;
        color: #b93535;
        cursor: pointer;
    }
</style>