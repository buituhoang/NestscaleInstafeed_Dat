import {createApp, h} from 'vue/dist/vue.esm-bundler';
import 'ant-design-vue/dist/antd.css';
import FeedShopify from "./components/FeedShopify.vue";

const vues = document.getElementsByClassName("app-shopify-id");

for (let vue of vues){
    let feed_id = vue.getAttribute('feed_id')
    var app_bundle = createApp({
        name: 'AppShopify',
        render: () => h(FeedShopify,{data:{feed_id:feed_id}})
    })

    app_bundle.mount(vue)
}
