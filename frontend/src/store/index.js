import Vue from 'vue'
import Vuex from 'vuex'

// modules
import auth from './modules/auth'
import files from './modules/files'
import alerts from './modules/alerts'
import appSettings from './modules/appSettings'
import filesListOptions from './modules/filesListOptions'

Vue.use(Vuex);

const state = {
    sideNavDrawer: true,

};
const getters = {
    SIDENAV_DRAWER: state => {
        return state.sideNavDrawer;
    },
};
const mutations = {
    CHANGE_SIDENAV_DRAWER: (state, payload) => {
        state.sideNavDrawer = payload
    },
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
        filesListOptions,
    },
    plugins: [],
});