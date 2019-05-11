import Vue from 'vue'
import Vuex from 'vuex'
import files from './modules/files'

Vue.use(Vuex);

const state = {};
const getters = {};
const mutations = {};
const actions = {};

export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions,
    modules: {
        files,
    }
});