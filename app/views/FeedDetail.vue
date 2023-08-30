<template>
  <div class="feed">
    <div class="customize">
      <div class="title">Customize</div>
      <div class="input-row">
        <div class="customize-item w-100">
          <label>FEED TITLE</label>
          <input type="text" v-model="feed_setting.title">
        </div>
      </div>

      <div class="input-row">
        <div class="customize-item w-40">
          <label>POST SPACING</label>
          <select v-model="feed_setting.post_spacing">
            <option value="0">No spacing</option>
            <option value="10">Small</option>
            <option value="20">Medium</option>
            <option value="30">Large</option>
          </select>
        </div>
      </div>

      <div class="input-row">
        <div class="customize-item w-50">
          <label>LAYOUT</label>
          <select v-model="feed_setting.layout">
            <option value="grid-squares">Grid Squares</option>
            <option value="grid-tiles">Grid Tiles</option>
            <option value="slider-squares">Slider Squares</option>
            <option value="slider-tiles">Slider Tiles</option>
          </select>
        </div>
        <div class="customize-item w-50">
          <label>CONFIGURATION</label>
          <select v-model="feed_setting.configuration">
            <option value="manual">Manual</option>
            <option value="auto">Auto</option>
          </select>
        </div>
      </div>

      <div class="input-row">
        <div class="customize-item w-50">
          <label>SLIDER PAGES</label>
          <input type="number" v-model="feed_setting.slider_pages">
        </div>
        <div class="customize-item w-50">
          <label>NUMBER OF POSTS</label>
          <input :disabled="feed_setting.configuration=='auto'" type="number" v-model="feed_setting.number_of_posts">
        </div>
      </div>
    </div>

    <div class="preview">
      <div class="title">Preview</div>
      <FeedComponent :posts="posts" :feed_setting="feed_setting"/>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import FeedComponent from "../components/FeedComponent.vue";

export default {
  components: {FeedComponent},
  data(){
    return{
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
  watch:{
    "feed_setting.number_of_posts"(newValue,oldValue){
      if (newValue > 8 || newValue < 1){
        this.feed_setting.number_of_posts = oldValue
      }else{
        axios.post('/feed/change/number_of_posts',{
          jsonrpc:2.0,
          params:{
            feed_id: parseInt(this.$route.params.id),
            number_of_posts:newValue
          }
        })
      }
    },
    "feed_setting.slider_pages"(newValue,oldValue){
      if (newValue > 4 || newValue < 1){
        this.feed_setting.slider_pages = oldValue
      }else{
        axios.post('/feed/change/slider_pages',{
          jsonrpc:2.0,
          params:{
            feed_id: parseInt(this.$route.params.id),
            slider_pages:newValue
          }
        })
      }
    },
    "feed_setting.configuration"(newValue,oldValue){
      axios.post('/feed/change/configuration',{
          jsonrpc:2.0,
          params:{
            feed_id: parseInt(this.$route.params.id),
            configuration:newValue
          }
        })
      if (newValue == 'auto'){
        this.feed_setting.number_of_posts = 3
      }
    },
    'feed_setting.title'(newValue,oldValue){
      axios.post('/feed/change/title',{
        jsonrpc:2.0,
        params:{
          feed_id: parseInt(this.$route.params.id),
          title:newValue
        }
      })
    },
    'feed_setting.post_spacing'(newValue,oldValue){
      axios.post('/feed/change/post_spacing',{
        jsonrpc:2.0,
        params:{
          feed_id: parseInt(this.$route.params.id),
          post_spacing:newValue
        }
      })
    },
    'feed_setting.layout'(newValue,oldValue){
      axios.post('/feed/change/layout',{
        jsonrpc:2.0,
        params:{
          feed_id: parseInt(this.$route.params.id),
          layout:newValue
        }
      })
    }
  },
  mounted() {
    axios.post('/feed/posts',{
      jsonrpc:2.0,
      params:{
        feed_id:this.$route.params.id
      }
    }).then(res => {
      this.posts = JSON.parse(res.data.result)['posts']
      this.feed_setting = JSON.parse(res.data.result)['setting']
    })
  }
};
</script>

<style scoped>
  .feed{
    width: 100%;
    display: flex;
    padding: 30px;
  }

  .customize{
    width: 45%;
  }

  .title{
    font-weight: 600;
    font-size: 18px;
    margin-left: 20px;
  }

  .preview{
    width: 55%;
    overflow-y: scroll;
  }

  .input-row{
    margin: 10px 0 30px;
    width: 100%;
    display: flex;
  }

  .customize-item{
    margin-right: 5%;
  }

  .customize-item-checkbox{
    margin-right: 5%;
  }

  .customize-item label{
    display: block;
    text-transform: uppercase;
  }

  .input-row input[type='text'],input[type='number'],select{
    width: 100%;
  }

  input[type='checkbox']{
    margin-left: 20px;
  }

  .save-feed-btn{
    border:none;
    background: #5ec25e;
    color:white;
    padding: 5px 20px;
    font-weight: 500;
    border-radius: 4px;
    cursor: pointer;
  }
</style>