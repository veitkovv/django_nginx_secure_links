import Vue from 'vue'
import Vuex from 'vuex'
import apollo from '../src/apolloClient'
import gql from 'graphql-tag'

Vue.use(Vuex);

const state = {
    files: []
};

const getters = {
    FILES: state => {
        return state.files;
    }
};

const mutations = {
    SET_FILES: (state, payload) => {
        state.files = payload
    },
    ADD_FILE: (state, payload) => {
        state.files.push(payload)
    }
};

const actions = {
    async getFiles({commit}) {
        const response = await apollo.query({
            query: gql`query {
                          files {
                            size
                            filename
                            modified
                            url
                            fileType
                            isFolder
                            hasUrl
                          }
                        }
                        `
        });
        commit('SET_FILES', response.data.files)
    },
};

export const store = new Vuex.Store({
    state,
    getters,
    mutations,
    actions
});