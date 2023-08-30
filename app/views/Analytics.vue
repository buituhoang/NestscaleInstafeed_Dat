<template>
  analytics
</template>

<script>
export default {
  mounted() {
      window.fbAsyncInit = function() {
      FB.init({
        appId: 'your-app-id',
        autoLogAppEvents: true,
        xfbml: true,
        version: 'v17.0'
        });
      };
  }
}
</script>
<style>

</style>