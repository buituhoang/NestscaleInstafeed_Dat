<template>
  <header>
    <div class="logo-connect">
      <img src="/instafeed/static/images/logo/fb.png" alt="Logo">
      <img src="/instafeed/static/images/logo/ins.png" alt="Logo">
    </div>
    <router-link :to="{name:'Dashboard'}" class="logo">
      <img src="/instafeed/static/images/logo/instafeed.png" alt="Logo">
      <span>Instafeed</span>
    </router-link>
    <div class="header-right">
      <div class="ask">
        <img @click="check" src="/instafeed/static/images/widgets/ask.png" alt="">
      </div>
      <div class="notification">
        <img src="/instafeed/static/images/widgets/notification.png" alt="">
        <div class="have-notification"></div>
      </div>
      <div class="logout">
        <img @click="logout" src="/instafeed/static/images/widgets/ava.png" alt="">
      </div>
    </div>
  </header>
</template>

<script>
import axios from "axios";

export default {
  methods:{
      logout(){
          window.location.href = '/web/session/logout'
      },
      check(){
        axios.post('/check/scrip_tag',{
          jsonrpc:'2.0',
          params:{}
        })
      }
  }
}
</script>

<style>
  header{
    background: #b079cb;
    height: 83px;
    display: flex;
    justify-content: space-between;
  }
  .logo-connect{
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .logo-connect img{
    width: 24px;
    height: 24px;
    margin-left: 20px;
  }
  .logo{
    display: flex;
    align-items: center;
    font-weight: 600;
    color: #17181A;
  }
  .logo img{
    font-family: 'Kanit';
    height: 46px;
    width: 46px;
    margin-right: 12px;
    border-radius: 50%;
    background: black;
  }
  .logo span{
    font-size: 40px;
    font-style: italic;
    letter-spacing: 3px;
    color:white;
  }
  .have-notification{
    /* width: 6px;
    height: 6px;
    border-radius: 50%;
    background: red; */
  }
  .header-right{
    display: flex;
    align-items: center;
    margin-right: 25px;
  }
  .header-right div{
    margin-left: 29px;
  }

  .logout{
    cursor: pointer;
  }
</style>