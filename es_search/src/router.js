import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

let index=()=>import('./views/search')


export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path:'/',
      redirect:'/search'
    },
    // 搜索页面
    {
      path:'/search',
      name:"search",
      component:index
    },

    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (about.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import(/* webpackChunkName: "about" */ './views/About.vue')
    // },
  ]
})
