<template>
  <div class="media-source content">
    <div class="main">
      <div class="head">
        <input v-model="search" type="text" class="search" placeholder="Search by feed name">
        <router-link :to="{name:'FeedCreate'}" class="make-src-btn">
          New feed
        </router-link>
      </div>
      <div class="table">
        <Table :dataSource="dataSourceSearch" :columns="columns">
          <template #bodyCell="{ column, record }">
            <template v-if="column.key === 'source_name'">
              <img class="platform-logo" v-if="record.platform === 'instagram'" src="/instafeed/static/images/logo/ins.png">
              <img class="platform-logo" v-if="record.platform === 'tiktok'" src="/instafeed/static/images/logo/tiktok.png">
              {{ record.source_name }}
            </template>
            <template v-if="column.key === 'action'">
              <i class="pointer fa-solid fa-pencil" @click="$router.push({name:'FeedDetail',params:{id:record.id}})"></i>
              <i class="pointer fa-solid fa-trash" @click="remove_feed(record.id)"></i>
            </template>
          </template>
        </Table>
      </div>
    </div>
  </div>
</template>

<script>
import {Table} from "ant-design-vue";
import axios from "axios";

export default {
  components: {Table},
  methods:{
    remove_feed(feed_id){
      axios.post('/feed/remove',{
        jsonrpc:2.0,
        params:{
          feed_id:feed_id
        }
      }).then(()=>{
        this.dataSource.splice(this.dataSource.findIndex(feed => feed.id==feed_id),1)
      })
    }
  },
  data(){
    return{
      search:'',
      dataSource: [],
      columns: [
        {
          title: 'Feed name',
          dataIndex: 'feed_name',
          key: 'feed_name',
        },
        {
          title: 'Feed id',
          dataIndex: 'feed_id',
          key: 'feed_id',
        },
        {
          title: 'Media items',
          dataIndex: 'media_items',
          key: 'media_items',
        },
        {
          title: 'Media source',
          dataIndex: 'media_source',
          key: 'media_source',
        },
        {
          title: 'Last update',
          dataIndex: 'last_update',
          key: 'last_update',
        },
        {
          dataIndex: 'action',
          key: 'action',
        }
      ],
    }
  },
  computed:{
    dataSourceSearch(){
      return this.dataSource.filter(metaSrc => metaSrc['feed_name'].includes(this.search))
    }
  },
  mounted() {
    axios.post('/feed/list',{
      jsonrpc:2.0,
      params:{}
    }).then(res=> this.dataSource = JSON.parse(res.data.result))
  }
};
</script>

<style scoped>
  .main{
    width:100%;
    padding: 30px 50px;
  }
  .head{
    width:100%;
    display:flex;
    justify-content: space-between;
  }

  .search{

  }

  .table{
    margin-top: 30px;
  }

  .platform-logo{
    width: 20px;
    height: 20px;
    margin-right: 10px;
  }

  .fa-trash{
    color: #ff3d3d;
    margin-left: 20px;
  }
</style>