import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import apolloProvider from './vue-apollo'
import {store} from '../store';


Vue.config.productionTip = false

new Vue({
  apolloProvider,
  store,
  render: h => h(App)
}).$mount('#app')
