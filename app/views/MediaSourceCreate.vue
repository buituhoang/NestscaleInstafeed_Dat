<template>
  <div class="media-source-create content">

    <div class="main">
      <div class="head">
        <router-link :to="{name:'MediaSource'}" class="back">
          &lt;
        </router-link>
        <button @click="create_media_source">Save</button>
      </div>

      <div class="title">Source Name</div>
      <input type="text" placeholder="Name media source" v-model="media_source_name" required>

      <div class="title">Social Platform</div>
      <div class="select">
        <div @click="change_platform('tiktok')" :class="{selected:isTiktok}" class="select-item">
          <img src="/instafeed/static/images/logo/tiktok.png"> Tiktok
        </div>
        <div @click="change_platform('instagram')" :class="{selected:isInstagram}" class="select-item">
          <img src="/instafeed/static/images/logo/ins.png"> Instagram
        </div>
      </div>

      <div class="title">Source Type</div>
      <div class="select">
        <div @click="change_source_type('personal_account')" :class="{selected:isPersonalAcount}" class="select-item">
          <i class="fa-solid fa-user"></i> Personal account
        </div>
        <div @click="change_source_type('hashtag')" :class="{selected:isHashtag}" class="select-item"># Hashtag</div>
        <div @click="change_source_type('mention')" :class="{selected:isMention}" class="select-item">@ Mention</div>
      </div>
      <input class="source-type-input" type="text" v-model="hashtag" v-if="isHashtag" placeholder="Hashtag">
      <input class="source-type-input" type="text" v-model="mention" v-if="isMention" placeholder="Mention">
      <div class="title">Select Acount</div>
      <div v-for="social_account in social_accounts">
        <div v-if="noneSocialAcount">
          You haven't connect {{social_platform}} acount. <span class="connect" @click="connect_social(this.social_platform)">Click here to connect</span>
        </div>
        <div class="social-account" v-if="social_account.platform.toLowerCase() == social_platform">
          <input type="radio" v-model="selected_id_account" :value="social_account.id">
          <img :src="social_account.profile_img">
          <div class="name">
            <div class="platform">{{social_account.platform}}</div>
            <div class="username">{{social_account.username}}</div>
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
      media_source_name:'',
      social_platform:'tiktok',
      source_type:'personal_account',
      social_accounts:[],
      hashtag:'',
      mention:'',
      selected_id_account:null,
    }
  },
  methods:{
    change_platform(platform){
      this.social_platform = platform
    },
    change_source_type(source_type){
      this.source_type = source_type
    },
    connect_social(social_platform){
      if(social_platform === 'tiktok'){
        window.location.href = '/tiktok/instafeed/auth'
      }else if (social_platform === 'instagram'){
        window.location.href = 'https://odoo.website/facebook/instafeed/auth'
      }
    },
    create_media_source(){
      if(this.media_source_name && this.selected_id_account){
        axios.post('/media_source/create',{
          jsonprc:2.0,
          params:{
            name:this.media_source_name,
            platform:this.social_platform,
            id:this.selected_id_account
          }
        })
        .then(res => {
          this.$router.push({name:'MediaSource'})
        })
      }
    }
  },
  computed:{
    isTiktok(){
      return this.social_platform == 'tiktok'
    },
    isInstagram(){
      return this.social_platform == 'instagram'
    },
    isPersonalAcount(){
      return this.source_type == 'personal_account'
    },
    isHashtag(){
      return this.source_type == 'hashtag'
    },
    isMention(){
      return this.source_type == 'mention'
    },
    noneSocialAcount(){
      let social_acount_platform = this.social_accounts.filter(social_account => social_account.platform.toLowerCase() == this.social_platform)

      if (social_acount_platform.length > 0 ){
        return false
      }
      return true
    }
  },
  mounted() {
    axios.post('/social/info',{
      jsonprc:2.0,
      pamrams:{}
    })
    .then(res => this.social_accounts = JSON.parse(res.data.result))
  }
};
</script>

<style scoped>
  .main{
    width: 60%;
    margin:100px auto;
  }

  .head{
    display: flex;
    justify-content: space-between;
  }

  .title{
    margin-top: 20px;
    font-size: 20px;
    font-weight: 500;
  }
  .select{
    display: flex;
  }

  .select-item{
    cursor: pointer;
    border-radius: 3px;
    border: 1px solid grey;
    padding: 10px;
    margin-right: 20px;
  }
  .select-item img{
    width: 20px;
    height: 20px;
  }
  .selected{
    border: 2px solid black;
    font-weight: 500;
  }
  .social-account{
    display: flex;
  }

  .social-account img{
    width: 50px;
    height: 50px;
    border-radius: 100%;
    margin-left: 20px;
  }

  .name{
    margin-left: 20px;
  }

  .platform{
    color: grey;
  }
  .name{
    font-weight: 500;
  }

  .source-type-input{
    margin-top: 10px;
    width: 500px;
  }

  .connect{
    cursor: pointer;
    font-weight: bold;
  }
</style>