<template>
  <div class="media-source content">
    <div class="main">
      <div class="head">
        <input v-model="search" type="text" class="search" placeholder="Search by source name">
        <router-link :to="{name:'MediaSourceCreate'}" class="make-src-btn">
          New media source
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
              <i class="pointer fa-solid fa-pencil" @click="$router.push({name:'MediaSourceDetail',params:{id:record.id}})"></i>
              <i class="pointer fa-solid fa-trash" @click="remove_media_source(record.id)"></i>
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
    remove_media_source(media_source_id){
      axios.post('/media_source/remove',{
        jsonrpc:2.0,
        params:{
          media_source_id:media_source_id
        }
      }).then(()=>{
        this.dataSource.splice(this.dataSource.findIndex(media_source => media_source.id==media_source_id),1)
      })
    }
  },
  data(){
    return{
      search:'',
      dataSource: [],
      columns: [
        {
          title: 'Source name',
          dataIndex: 'source_name',
          key: 'source_name',
        },
        {
          title: 'Source account',
          dataIndex: 'source_account',
          key: 'source_account',
        },
        {
          title: 'Media items',
          dataIndex: 'media_items',
          key: 'media_items',
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
      return this.dataSource.filter(metaSrc => metaSrc['source_name'].includes(this.search))
    }
  },
  mounted() {
    axios.post('/media_source/list',{
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