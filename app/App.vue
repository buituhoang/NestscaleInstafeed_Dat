<template>
    <Header/>
    <div class="wrapper">
        <Navbar/>
        <router-view/>
    </div>
</template>

<script>
import Header from "./components/Header.vue";
import Navbar from "./components/Navbar.vue";

export default {
    name: "App",
    components: {Navbar, Header},
    data() {
        return {};
    },
    methods: {
        test_method: function () {
            console.log('Test')
        }
    },
    computed: {},
    async mounted() {}
}
</script>

<style>
    .wrapper{
        display: flex;
        height: 91vh;
    }
</style>
<style src="./css/main.css"></style>