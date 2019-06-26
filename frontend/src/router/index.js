import Vue from 'vue'
import Router from 'vue-router'
import {store} from '../store/index'

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: '/',
            component: () => import('../components/pages/Root/Root')
        },
        {
            path: '/login',
            component: () => import('../components/pages/Login')
        },
        {
            path: '/about',
            component: () => import('../components/pages/About')
        },
        {
            path: '/settings',
            component: () => import('../components/pages/AppSettings')
        },
        {
            path: '/calendar',
            component: () => import('../components/pages/AppCalendar')
        },
        {
            path: '*',
            component: () => import('../components/pages/NotFound')
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