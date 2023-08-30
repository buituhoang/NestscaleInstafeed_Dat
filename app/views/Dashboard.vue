<template>
  <div class="content">
    <div class="welcome">WELCOME, {{ username }}!</div>
    <div class="product-list">
      <!-- Header -->
      <div class="product-list-header product-list-row">
        <div class="check-box">
          #
        </div>
        <div class="title">Widget Title</div>
        <div class="description">Widget Description</div>
        <div class="price">Products included</div>
        <div class="compare">Total Price</div>
        <div class="stock">Status</div>
      </div>
      <!-- item -->
      <div class="product-list-item-wrapper">
        <div class="product-list-item product-list-row" v-for="n in widgets.length" :key="n">
          <div class="check-box">
            {{n}}
          </div>
          <div class="title">
            {{ widgets[n-1].title }}
          </div>
          <div class="description">{{ widgets[n-1].description }}</div>
          <div class="price">{{ widgets[n-1].products_num }}</div>
          <div class="compare">{{ widgets[n-1].total_price }}</div>
          <div class="stock"><Switch @change="toggleStatus(widgets[n-1].id)" v-model:checked="widgets[n-1].status" checked-children="ON" un-checked-children="OFF"/></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {Switch} from "ant-design-vue";

export default {
  components: {Switch},
  data(){
    return{
      widgets:[],
      username:window.app_settings.user_name
    }
  },
  methods:{
    toggleStatus(id){
      axios.post('/bundle/toggle_status',{
        jsonrpc:2.0,
        params:{
          id:id
        }
      })
    }
  },
  mounted() {
    axios.post('/widget/info',{
      jsonrpc:2.0,
      params:{}
    })
    .then(res => this.widgets = JSON.parse(res.data.result))
    .catch(e=>{
      console.log(e)
    })
  }
};
</script>

<style scoped>
.welcome {
  margin: 51px 57px;
  font-weight: 600;
  font-size: 27px;
  text-transform: uppercase;
}

.product-list{
    margin: 30px 50px;
    line-height: 34px;
    border-bottom: 1px solid #E2E2E2;
  }

  .product-list-row{
    width: 100%;
    display: flex;
    border-top: 1px solid #E2E2E2;
  }

  .product-list-header{
    font-weight: 700;
    border-bottom: 1px solid #E2E2E2;
  }
  .product-list-item-wrapper{
    height: 174px;
    overflow-y: scroll;
  }
  .product-list-item-disable div{
    font-weight: 400;
    color: #D9D9D9;
  }
  .product-list .check-box{
    width: 5%;
  }
  .product-list .title{
    width: 20%;
  }
  .product-list .description{
    width: 30%;
  }
  .product-list .price{
    width: 15%;
  }
  .product-list .compare{
    width: 15%;
  }
  .product-list .stock{
    width: 15%;
  }
</style>