import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import apolloProvider from './vue-apollo'

Vue.config.productionTip = false

new Vue({
  apolloProvider: apolloProvider,
  render: h => h(App)
}).$mount('#app')
