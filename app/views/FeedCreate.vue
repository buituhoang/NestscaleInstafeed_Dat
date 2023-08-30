<template>
  <div class="media-source-create content">

    <div class="main">
      <div class="head">
        <router-link :to="{name:'Feed'}" class="back">
          &lt;
        </router-link>
        <button @click="createFeed">Save</button>
      </div>

      <div class="title">Feed Name</div>
      <input type="text" placeholder="Name feed" v-model="feed_name" required>

      <div class="space-between">
        <div class="title">Select media source</div>
        <div @click="open_modal" class="open-modal">+ Add media source</div>
      </div>

      <div class="table">
        <Table :dataSource="dataSourceChoosen" :columns="columns">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'source_name'">
                <img class="platform-logo" v-if="record.platform === 'instagram'" src="/instafeed/static/images/logo/ins.png">
                <img class="platform-logo" v-if="record.platform === 'tiktok'" src="/instafeed/static/images/logo/tiktok.png">
                {{ record.source_name }}
              </template>
              <template v-if="column.key === 'source_type'">
                Account
              </template>
              <template v-if="column.key === 'action'">
                <i class="pointer fa-solid fa-pencil" @click="$router.push({name:'MediaSourceDetail',params:{id:record.id}})"></i>
                <i class="pointer fa-solid fa-trash" @click="remove_media_source(record.id)"></i>
              </template>
            </template>
          </Table>

        <Modal width="780px" v-model:visible="open" title="Basic Modal" :footer="null">
          <input v-model="search" type="text" class="media-source-search" placeholder="Search products">
          <Table :dataSource="dataSourceSearch" :columns="columns">
            <template #bodyCell="{ column, record }">
              <template v-if="column.key === 'checkbox'">
                <input v-model="record.checkbox" type="checkbox">
              </template>
              <template v-if="column.key === 'source_name'">
                <img class="platform-logo" v-if="record.platform === 'instagram'" src="/instafeed/static/images/logo/ins.png">
                <img class="platform-logo" v-if="record.platform === 'tiktok'" src="/instafeed/static/images/logo/tiktok.png">
                {{ record.source_name }}
              </template>
              <template v-if="column.key === 'source_type'">
                Account
              </template>
              <template v-if="column.key === 'action'">
                <i class="pointer fa-solid fa-pencil" @click="$router.push({name:'MediaSourceDetail',params:{id:record.id}})"></i>
                <i class="pointer fa-solid fa-trash" @click="remove_media_source(record.id)"></i>
              </template>
            </template>
          </Table>
        </Modal>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import {Table,Modal,Button} from "ant-design-vue";

export default {
  components: {Table,Modal,Button},
  data(){
    return{
      search:'',
      open:false,
      dataSource:[],
      feed_name: '',
      columns: [
        {
          dataIndex: 'checkbox',
          key: 'checkbox',
        },
        {
          title: 'Source name',
          dataIndex: 'source_name',
          key: 'source_name',
        },
        {
          title: 'Source type',
          dataIndex: 'source_type',
          key: 'source_type',
        },
        {
          title: 'Source detail',
          dataIndex: 'source_account',
          key: 'source_account'
        },
        {
          title: 'Media items',
          dataIndex: 'media_items',
          key: 'media_items'
        }
      ]
    }
  },methods:{
    open_modal(){
      this.open = true
    },
    handleCancel(){
      visible.value = false;
    },
    createFeed(){
      let meida_source_ids = []
      for(let media_source of this.dataSource){
        if(media_source['checkbox'] == true){
          meida_source_ids.push(media_source['id'])
        }
      }
      axios.post('/feed/create',{
        jsonrpc:2.0,
        params:{
          feed_name: this.feed_name,
          media_source_ids: meida_source_ids
        }
      }).then((res) =>{
        this.$router.push({name:'FeedDetail',params:{id:JSON.parse(res.data.result)['feed_id']}})
      })
    }
  },
  computed:{
    dataSourceSearch(){
      return this.dataSource.filter(metaSrc => metaSrc['source_name'].includes(this.search))
    },
    dataSourceChoosen(){
      return this.dataSource.filter(metaSrc => metaSrc['checkbox'] == true)
    }
  },
  async mounted() {
    await axios.post('/media_source/list',{
      jsonrpc:2.0,
      params:{}
    }).then(res=> this.dataSource = JSON.parse(res.data.result))

    for (let data of this.dataSource){
      data['checkbox'] = false
    }
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

.open-modal{
  color: #2f2fc0;
  cursor: pointer;
}

.ant-btn-primary{
  background: black;
}

.ant-btn-primary>span{
  color:white !important;
}

.media-source-search{
  margin: 10px auto;
  width: 90%;
  display: block;
}

  .platform-logo{
    width: 20px;
    height: 20px;
    margin-right: 10px;
  }
</style>