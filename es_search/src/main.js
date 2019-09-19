import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

Vue.config.productionTip = false

import './static/css/reset.css'
import 'iview/dist/styles/iview.css'
import {Input,Button,Message,Notice,Layout,Header,Content,Footer,Page,Tabs,TabPane,DropdownMenu,
  DropdownItem,Dropdown} from 'iview'
Vue.component(Input.name,Input)
Vue.component(Button.name,Button)
Vue.component(Layout.name,Layout)
Vue.component(Header.name,Header)
Vue.component(Content.name,Content)
Vue.component(Footer.name,Footer)
Vue.component(Page.name,Page)
Vue.component(Tabs.name,Tabs)
Vue.component(TabPane.name,TabPane)
Vue.component(Dropdown.name,Dropdown)
Vue.component(DropdownMenu.name,DropdownMenu)
Vue.component(DropdownItem.name,DropdownItem)
Vue.prototype.$Message=Message
Vue.prototype.$Notice=Notice

import VueCookies from 'vue-cookies'
Vue.use(VueCookies)
import VueClipboard from 'vue-clipboard2'
Vue.use(VueClipboard)


new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
