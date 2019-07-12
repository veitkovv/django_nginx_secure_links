import Vue from 'vue'
import Vuetify from 'vuetify/lib'
import 'vuetify/src/stylus/app.styl'
import '@fortawesome/fontawesome-free/css/all.css' // Ensure you are using css-loader

Vue.use(Vuetify, {
    iconfont: 'fa', // 'md' || 'mdi' || 'fa' || 'fa4'
    theme: {
        "primary": "#1976D2",
        "secondary": "#424242",
        "accent": "#82B1FF",
        "error": "#FF5252",
        "info": "#2196F3",
        "success": "#4CAF50",
        "warning": "#FB8C00"
    }
})
