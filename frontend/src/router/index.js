import Vue from 'vue'
import Router from 'vue-router'
import {store} from '../store/index'

Vue.use(Router);

const router = new Router({
    routes: [
        {
            path: '/',
            icon: 'home',
            name: 'Главная',
            component: () => import('../components/pages/Root/Root')
        },
        {
            path: '/about',
            icon: 'info',
            name: 'О приложении',
            component: () => import('../components/pages/About')
        },
        {
            path: '/settings',
            icon: 'settings',
            name: 'Настройки',
            component: () => import('../components/pages/AppSettings')
        },
        {
            path: '/login',
            icon: 'exit_to_app',
            name: 'Авторизация',
            component: () => import('../components/pages/Login')
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