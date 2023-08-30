<template>
  <div class="content media-source-detail">
    <div class="space-between">
      <router-link :to="{name:'MediaSource'}" class="back">
        &lt;
      </router-link>
      <div class="flex align-items-center">
        <div class="number-video-selected">{{ selected_post_number }} videos selected</div>
        <div class="select-all">
          <input v-model="select_all" type="checkbox" name="" id=""><label>Select all</label>
        </div>
        <div class="action-btn">
          <div @click="hide_post" class="hide pointer">Hide</div>
          <span>/</span>
          <div @click="show_post" class="show pointer">Show</div>
        </div>
      </div>
    </div>

    <div>
      <div class="customize-item">
        <label>ON POST CLICK</label>
        <select v-model="on_post_click">
          <option value="popup">Open popup / show product</option>
          <option value="insta">Go to <span v-if="post_list['platform']=='instagram'">instagram</span><span
              v-if="post_list['platform']=='tiktok'">tiktok</span></option>
          <option value="none">Do nothing</option>
        </select>
      </div>

      <div class="input-row">
        <div class="customize-item-checkbox w-50">
          <label>SHOW LIKE</label>
          <input type="checkbox" v-model="show_like">
        </div>
        <div class="customize-item-checkbox w-50">
          <label>SHOW COMMENT</label>
          <input type="checkbox" v-model="show_comment">
        </div>
      </div>
    </div>
    <div class="post-list">
      <div class="post" v-for="post in post_list['list']">
        <FeedPost
            :customize_hotspot="true"
            :post="post"
            :platform="post_list['platform']"
            :click_type="on_post_click"
            :show_like="show_like"
            :show_comment="show_comment"
        />
        <input type="checkbox" class="post-check" v-model="selected_post[post['post_id']]">
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import FeedPost from "../components/FeedPost.vue";
export default {
  components: {FeedPost},
  data() {
    return {
      select_all:false,
      post_list: [],
      selected_post:{},
      on_post_click: 'popup',
      show_like: false,
      show_comment: false
    }
  },
  computed:{
    selected_post_number(){
      let count = 0
      for (const [key, value] of Object.entries(this.selected_post)){
        if (value) {
          count++
        }
      }
      return count
    }
  },
  methods:{
    hide_post(){
      let selected_post_list = []
      for (const [key, value] of Object.entries(this.selected_post)){
        if (value) {
          selected_post_list.push(parseInt(key))
        }
      }
      axios.post('/media_source/posts/hide', {
        jsonrpc: 2.0,
        params: {
          selected_post:selected_post_list,
          media_source_id:parseInt(this.$route.params.id)
        }
      }).then(res => {
          for (const [key, value] of Object.entries(this.selected_post)){
          if (value) {
            for (let post of this.post_list['list']){
              if(this.selected_post[post['post_id']]){
                post['is_showed'] = false
              }
            }
          }
        }
      })
    },
    show_post(){
      let selected_post_list = []
      for (const [key, value] of Object.entries(this.selected_post)){
        if (value) {
          selected_post_list.push(parseInt(key))
        }
      }
      axios.post('/media_source/posts/show', {
        jsonrpc: 2.0,
        params: {
          selected_post:selected_post_list,
          media_source_id:parseInt(this.$route.params.id)
        }
      }).then(res => {
        for (const [key, value] of Object.entries(this.selected_post)) {
          if (value) {
            for (let post of this.post_list['list']) {
              if (this.selected_post[post['post_id']]) {
                post['is_showed'] = true
              }
            }
          }
        }
      })
    }
  },
  watch:{
    select_all(newSelect,oldSelect){
      for (let post_id of Object.keys(this.selected_post)){
        this.selected_post[post_id] = newSelect
      }
    },
    on_post_click(newValue,oldValue){
      axios.post('/media_source/change/on_post_click',{
        jsonrpc:2.0,
        params:{
          media_source_id: parseInt(this.$route.params.id),
          on_post_click:newValue
        }
      })
    },
    show_comment(newValue,oldValue){
      axios.post('/media_source/change/show_comment',{
        jsonrpc:2.0,
        params:{
          media_source_id: parseInt(this.$route.params.id),
          show_comment:newValue
        }
      })
    },
    show_like(newValue,oldValue){
      axios.post('/media_source/change/show_like',{
        jsonrpc:2.0,
        params:{
          media_source_id: parseInt(this.$route.params.id),
          show_like:newValue
        }
      })
    }

  },
  async mounted() {
    await axios.post('/media_source/posts', {
      jsonrpc: 2.0,
      params: {
        media_source_id: parseInt(this.$route.params.id)
      }
    }).then(res => this.post_list = JSON.parse(res.data.result))

    for (let post of this.post_list['list']){
      this.selected_post[post['post_id']] = false
    }

    this.on_post_click = this.post_list['setting']['on_post_click']
    this.show_comment = this.post_list['setting']['show_comment']
    this.show_like = this.post_list['setting']['show_like']
  }
};
</script>

<style scoped>
.media-source-detail {
  padding: 30px 100px;
}

.number-video-selected{
  color: #3333ff;
  margin-right: 40px;
}

.select-all{
  margin-right: 20px;
  padding: 5px;
  border-radius: 3px;
  border: 1px solid black;
}
.select-all input{
  margin-right: 10px;
}
.post-list {
  margin-top: 20px;
  display: grid;
  grid-gap: 20px;
  grid-template-columns: auto auto auto auto auto auto;
}

.post {
  aspect-ratio: 1 / 1.5;
  position: relative;
}

.post-check{
  top: 20px;
  right: 20px;
  position: absolute;
  z-index: 10;
}

iframe {
  height: 408px;
  width: 231px;
}

.customize-item {
  margin: 30px 0;
}

.customize-item label {
  display: block;
  text-transform: uppercase;
}

.customize-item-checkbox label {
  margin-right: 20px;
}

.input-row {
  margin: 10px 0 30px;
  width: 40%;
  display: flex;
}

.action-btn{
  display: flex;
}
</style>