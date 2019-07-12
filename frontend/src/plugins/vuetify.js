import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import '@fortawesome/fontawesome-free/css/all.css' // Ensure you are using css-loader

Vue.use(Vuetify, {
    iconfont: 'fa', // 'md' || 'mdi' || 'fa' || 'fa4'
    theme: {
        primary: '#673ab7',
        secondary: '#cddc39',
        accent: '#8bc34a',
        error: '#ff9800',
        warning: '#ffeb3b',
        info: '#009688',
        success: '#4caf50'

    }
})
