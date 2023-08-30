<template>
  <div class="shopify-bundle">
    <div v-for="bundle in bundles">
      <div class="bundle-contain">
        <Bundle :bundle="bundle"/>
      </div>
    </div>
  </div>
</template>

<script>
import Bundle from "./Bundle.vue";
import axios from "axios";

export default {
  components: {Bundle},
  data(){
    return{
      bundles:{}
    }
  },
  mounted() {
    axios.post('https://odoo.website/ui/bundle',{
        jsonrpc:2.0,
        params:{
          shop: window.Shopify.shop,
          variant: window.ShopifyAnalytics.meta.selectedVariantId
        }
    })
    .then(res => this.bundles = JSON.parse(res.data.result))
    .catch(e => console.log(e))
  }

}
</script>

<style>
  .bundle-contain{
    width: 1000px;
    margin : 50px auto 0;
    border-radius: 5px;
    border: 1px solid #BFBFBF;
    padding: 0 10%;
  }

  .flex{
      display: flex;
  }

  .space-between{
      justify-content: space-between;
  }
</style>