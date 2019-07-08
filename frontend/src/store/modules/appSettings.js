import {apolloClient} from '../../vue-apollo'
import DEFAULT_SETTINGS_QUERY from '../../graphql/DefaultSettings.gql'
import SET_URL_EXPIRES_MUTATION from '../../graphql/SetUrlExpires.gql'

function daysToSeconds(days) {
    return Math.floor(days * (3600 * 24));
}

function secondsToDays(seconds) {
    return Math.floor(seconds / (3600 * 24));
}

const state = {
    minUrlExpires: 0,
    maxUrlExpires: 0,
    UrlExpires: 0,
};

const getters = {
    MIN_URL_EXPIRES: state => {
        return secondsToDays(state.minUrlExpires)
    },
    MAX_URL_EXPIRES: state => {
        return secondsToDays(state.maxUrlExpires)
    },
    URL_EXPIRES: state => {
        return state.UrlExpires
    },
};

const mutations = {
    SET_MIN_URL_EXPIRES: (state, payload) => {
        state.minUrlExpires = payload
    },
    SET_MAX_URL_EXPIRES: (state, payload) => {
        state.maxUrlExpires = payload
    },
    SET_URL_EXPIRES: (state, payload) => {
        state.UrlExpires = payload
    }
};

const actions = {
    async fetchDefaultSettings({commit}) {
        const response = await apolloClient.query({
            query: DEFAULT_SETTINGS_QUERY,
        });
        commit('SET_MIN_URL_EXPIRES', response.data.minUrlExpires);
        commit('SET_MAX_URL_EXPIRES', response.data.maxUrlExpires)
    },

    async updateUrlExpires({commit}, newUrlExpires) {
        const response = await apolloClient.mutate({
            mutation: SET_URL_EXPIRES_MUTATION,
            variables: {
                newUrlExpires: daysToSeconds(newUrlExpires)
            }
        });
        commit('SET_URL_EXPIRES', secondsToDays(response.data.setUrlExpires.newUrlExpires))
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};