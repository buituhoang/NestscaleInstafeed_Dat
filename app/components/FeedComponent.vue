<template>
  <div class="feed-component">
    <div v-if="feed_setting.title" class="title">
       {{feed_setting.title}}
    </div>
    <div v-if="feed_setting.layout == 'grid-squares' || feed_setting.layout == 'grid-tiles'" class="feed-content" :style="{
      gridTemplateColumns: `repeat(${feed_setting.number_of_posts}, 1fr)`,
      gap: feed_setting.post_spacing+'px'
    }">

      <div v-if="feed_setting.layout == 'grid-squares'" v-for="n in number_of_posts_diplay" class="grid-squares-feed-img">
        <FeedPost  v-if="n<=posts.length" :post="posts[n-1]"
                   :click_type="posts[n-1].on_post_click"
                   :platform="posts[n-1].platform"
                   :show_like="posts[n-1].show_like"
                   :show_comment="posts[n-1].show_comment"/>
      </div>

      <div v-if="feed_setting.layout == 'grid-tiles'" v-for="n in number_of_posts_diplay" class="grid-tiles-feed-img">
        <FeedPost  v-if="n<=posts.length" :post="posts[n-1]"
                   :click_type="posts[n-1].on_post_click"
                   :platform="posts[n-1].platform"
                   :show_like="posts[n-1].show_like"
                   :show_comment="posts[n-1].show_comment"/>
      </div>

    </div>

     <Carousel  v-if="feed_setting.layout == 'slider-squares' || feed_setting.layout == 'slider-tiles'" arrows>
        <template #prevArrow>
          <div class="custom-slick-arrow" style="left: 10px; z-index: 1">
            <left-circle-outlined />
          </div>
        </template>
        <template #nextArrow>
          <div class="custom-slick-arrow" style="right: 10px">
            <right-circle-outlined />
          </div>
        </template>
        <div v-for="slide_number in number_of_slide" >
          <div class="feed-content" :style="{
            gridTemplateColumns: `repeat(${feed_setting.number_of_posts}, 1fr)`,
            gap: feed_setting.post_spacing+'px'
          }">
            <div v-if="feed_setting.layout == 'slider-squares'"  v-for="n in feed_setting.number_of_posts"  class="grid-squares-feed-img">
              <FeedPost v-if="(slide_number-1)*feed_setting.number_of_posts+n<=posts.length" :post="posts[(slide_number-1)*feed_setting.number_of_posts+n-1]"
                  :click_type="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].on_post_click"
                  :platform="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].platform"
                  :show_like="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].show_like"
                  :show_comment="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].show_comment"/>
            </div>

            <div v-if="feed_setting.layout == 'slider-tiles'" v-for="n in feed_setting.number_of_posts"  class="grid-tiles-feed-img">
              <FeedPost v-if="(slide_number-1)*feed_setting.number_of_posts+n<=posts.length" :post="posts[(slide_number-1)*feed_setting.number_of_posts+n-1]"
                  :click_type="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].on_post_click"
                  :platform="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].platform"
                  :show_like="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].show_like"
                  :show_comment="posts[(slide_number-1)*feed_setting.number_of_posts+n-1].show_comment"/>
            </div>
          </div>
        </div>
      </Carousel>
  </div>
</template>

<script>
  import { LeftCircleOutlined, RightCircleOutlined } from '@ant-design/icons-vue';
  import {Carousel} from "ant-design-vue";
  import FeedPost from "./FeedPost.vue";

  export default {
    components: {FeedPost, Carousel, LeftCircleOutlined, RightCircleOutlined},
    props:['posts','feed_setting'],
    computed:{
      number_of_posts_diplay(){
        let number_of_posts = this.posts.length < this.feed_setting.number_of_posts*this.feed_setting.slider_pages ? this.posts.length : this.feed_setting.number_of_posts*this.feed_setting.slider_pages

        return number_of_posts
      },
      number_of_slide(){
        return this.feed_setting.slider_pages < Math.ceil(this.posts.length/this.feed_setting.number_of_posts) ? this.feed_setting.slider_pages : Math.ceil(this.posts.length/this.feed_setting.number_of_posts)
      }
    }
  }
</script>

<style scoped>
  .title{
    padding: 20px;
    display: flex;
    justify-content: center;
    font-size: 20px;
    font-weight: 500;
  }

  .feed-content{
    display: grid;
  }

  .grid-squares-feed-img{
    aspect-ratio: 1 / 1;
    position: relative;
  }

  .grid-tiles-feed-img{
    aspect-ratio: 1 / 2;
    position: relative;
  }

  /* style carousel */

  :deep(.slick-arrow.custom-slick-arrow) {
    width: 25px;
    height: 25px;
    font-size: 25px;
    color: #fff;
    background-color: rgba(31, 45, 61, 0.11);
    transition: ease all 0.3s;
    opacity: 0.3;
    z-index: 1;
  }

  :deep(.slick-arrow.custom-slick-arrow) span, :deep(.slick-arrow.custom-slick-arrow) svg{
    width: 100%;
    height: 100%;
  }
  :deep(.slick-arrow.custom-slick-arrow:before) {
    display: none;
  }
  :deep(.slick-arrow.custom-slick-arrow:hover) {
    color: #fff;
    opacity: 0.5;
  }

  :deep(.slick-slide h3) {
    color: #fff;
  }
</style>
