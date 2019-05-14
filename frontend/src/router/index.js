import Vue from 'vue'
import Router from 'vue-router'
import {store} from '../../store/index'

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: '/',
            component: () => import('../components/FileList')
        },
        {
            path: '/login',
            component: () => import('../components/AppLogin')
        },
        {
            path: '*',
            component: () => import('../components/NotFound')
        }
    ],
    mode: 'history'
});

router.beforeEach((to, from, next) => {
    if (!store.getters.IS_AUTHENTICATED && to.path !== '/login') {
        next('/login')
    } else {
        next()
    }
});

export default router