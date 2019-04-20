import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'

Vue.use(Vuetify, {
    iconfont: 'md',
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
