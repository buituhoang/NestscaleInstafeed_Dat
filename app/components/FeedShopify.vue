<template>
  <div class="feed-shopify">
    Hello, this is feed shopify
    {{ feed_id}}
    <FeedComponent :posts="posts" :feed_setting="feed_setting"/>
  </div>
</template>

<script>
import axios from "axios";
import FeedComponent from "./FeedComponent.vue";

export default {
  components: {FeedComponent},
  data(){
    return{
      feed_id:this.$attrs.data.feed_id,
      posts:'',
      feed_setting:{
        title: '',
        post_spacing:0,
        layout:'grid-squares',
        configuration:'manual',
        number_of_posts: 3,
        slider_pages:1,
      }
    }
  },
  mounted() {
    axios.post('https://odoo.website/feed/posts',{
      jsonrpc:2.0,
      params:{
        hash_feed_id:this.feed_id,
      }
    }).then(res => {
      this.posts = JSON.parse(res.data.result)['posts']
      this.feed_setting = JSON.parse(res.data.result)['setting']
    }).catch(e=>{
      console.log(e)
    })
  }
}
</script>

<style>

</style>