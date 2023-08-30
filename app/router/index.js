import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Feed from '../views/Feed.vue'
import FeedDetail from '../views/FeedDetail.vue'
import FeedCreate from '../views/FeedCreate.vue'
import Association from '../views/Association.vue'
import ShopifyAssociation from '../views/ShopifyAssociation.vue'
import Analytics from '../views/Analytics.vue'
import MediaSource from '../views/MediaSource.vue'
import MediaSourceCreate from '../views/MediaSourceCreate.vue'
import MediaSourceDetail from '../views/MediaSourceDetail.vue'
import paths from  './paths'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: paths.Dashboard,
      name: 'Dashboard',
      component: Dashboard
    },
    {
      path: paths.Feed,
      name: 'Feed',
      component: Feed
    },
    {
      path: paths.FeedDetail,
      name: 'FeedDetail',
      component: FeedDetail
    },
    {
      path: paths.FeedCreate,
      name: 'FeedCreate',
      component: FeedCreate
    },
    {
      path: paths.Association,
      name: 'Association',
      component: Association
    }
    ,{
      path: paths.ShopifyAssociation,
      name: 'ShopifyAssociation',
      component: ShopifyAssociation
    },
    {
      path: paths.MediaSource,
      name: 'MediaSource',
      component: MediaSource
    },
    {
      path: paths.MediaSourceCreate,
      name: 'MediaSourceCreate',
      component: MediaSourceCreate
    },
    {
      path: paths.MediaSourceDetail,
      name: 'MediaSourceDetail',
      component: MediaSourceDetail
    },
    {
      path: paths.Analytics,
      name: 'Analytics',
      component: Analytics
    }
  ]
})

export default router
