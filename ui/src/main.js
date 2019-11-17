import Vue from 'vue'
import App from './App.vue'
import vuetify from "./vuetify"
import store from './store.js'
import router from './routers'


Vue.config.productionTip = false

new Vue({
  store,
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
