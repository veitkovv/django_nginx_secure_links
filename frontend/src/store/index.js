import Vue from 'vue'
import Vuex from 'vuex'
import createPersistedState from 'vuex-persistedstate';
// modules
import auth from './modules/auth'
import files from './modules/files'
import alerts from './modules/alerts'

Vue.use(Vuex);

const state = {
    sideNavDrawer: true
};
const getters = {
    SIDENAV_DRAWER: state => {
        return state.sideNavDrawer;
    }
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
    },
    plugins: [createPersistedState()],
});