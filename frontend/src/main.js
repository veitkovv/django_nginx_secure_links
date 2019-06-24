import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import apolloProvider from './vue-apollo'
import {store} from './store';
import router from './router'
import VueClipboard from 'vue-clipboard2'
import Notifications from 'vue-notification'

Vue.use(VueClipboard);
Vue.use(Notifications);


Vue.config.productionTip = false;

new Vue({
    apolloProvider,
    store,
    router,
    render: h => h(App)
}).$mount('#app');
