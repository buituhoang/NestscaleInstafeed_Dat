<template>
  <div class="navbar">
    <router-link :to="{name:'Dashboard'}" class="nav-item">
      <img src="" alt="">
      Dashboard
    </router-link>
    <router-link :to="{name:'Association'}" class="nav-item">
      <img src="" alt="">
      Association
    </router-link>
    <router-link :to="{name:'MediaSource'}" class="nav-item">
      <img src="" alt="">
      Media Source
    </router-link>
    <router-link :to="{name:'Feed'}" class="nav-item">
      <img src="" alt="">
      Feed
    </router-link>
    <router-link :to="{name:'Analytics'}" class="nav-item">
      <img src="" alt="">
      Analytics
    </router-link>
  </div>
</template>

<script>
export default {

}
</script>

<style scoped>
  .navbar{
      min-width: 276px;
      height: 100vh;
      background: #e5bfde;
  }
  .nav-item{
    padding: 19px 20px;
  }
  .nav-item.router-link-active{
    background: #de68df;
  }
  .nav-item img{
    height: 32px;
    width: 32px;
    border-radius: 50%;
    background: #d9d9d9;
  }
  a{
    display: block;
    color: black
  }
</style>