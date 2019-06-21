import {apolloClient} from '../../vue-apollo'
import DEFAULT_SETTINGS_QUERY from '../../graphql/DefaultSettings.gql'

const state = {
    appDefaultSettings: '',
    linkTTL: 0,
};

const getters = {
    DEFAULT_SETTINGS: state => {
        return state.appDefaultSettings
    },
    MIN_TTL: state => {
        // seconds -> days
        return Math.floor(state.appDefaultSettings.minTtl / (3600 * 24));
    },
    MAX_TTL: state => {
        // seconds -> days
        return Math.floor(state.appDefaultSettings.maxTtl / (3600 * 24));
    },
    LINK_TTL: state => {
        return state.linkTTL
    },
};

const mutations = {
    CHANGE_DEFAULT_SETTINGS: (state, payload) => {
        state.appDefaultSettings = payload
    },
    SET_LINK_TTL: (state, payload) => {
        state.linkTTL = payload
    }
};

const actions = {
    async fetchDefaultSettings({commit}) {
        const response = await apolloClient.query({
            query: DEFAULT_SETTINGS_QUERY,
        });
        commit('CHANGE_DEFAULT_SETTINGS', JSON.parse(JSON.parse(response.data.defaultSettings)))
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};