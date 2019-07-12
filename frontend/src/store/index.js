import Vue from 'vue'
import Vuex from 'vuex'

// modules
import auth from './modules/auth'
import files from './modules/files'
import alerts from './modules/alerts'
import appSettings from './modules/appSettings'

Vue.use(Vuex);

const state = {
    sideNavDrawer: true,
    withoutLinksOnly: false,
};
const getters = {
    SIDENAV_DRAWER: state => {
        return state.sideNavDrawer;
    },
    WITHOUT_LINKS_ONLY: state => {
        return state.withoutLinksOnly
    }
};
const mutations = {
    CHANGE_SIDENAV_DRAWER: (state, payload) => {
        state.sideNavDrawer = payload
    },
    CHANGE_WITHOUT_LINKS_ONLY: (state, payload) => {
        state.withoutLinksOnly = payload
    }
};
const actions = {
    changeSidenavDrawerState({commit}) {
        commit('CHANGE_SIDENAV_DRAWER', !this.getters.SIDENAV_DRAWER)
    },
    changeWithoutLinksOnly({commit}) {
        commit('CHANGE_WITHOUT_LINKS_ONLY', !this.getters.WITHOUT_LINKS_ONLY)
    }
};

export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    modules: {
        auth,
        files,
        alerts,
        appSettings,
    },
    plugins: [],
});