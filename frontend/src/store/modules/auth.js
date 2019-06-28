import {apolloClient} from '../../vue-apollo'
import LOGIN_MUTATION from '../../graphql/TokenAuth.gql'
import VERIFY_TOKEN_MUTATION from '../../graphql/VerifyToken.gql'
import CURRENT_USER from '../../graphql/Me.gql'

const state = {
    token: null,
    tokenData: null,
    currentUserData: null,
};

const getters = {
    TOKEN: state => {
        return state.token;
    },
    TOKEN_DATA: state => {
        return state.tokenData;
    },
    IS_AUTHENTICATED: state => {
        const now = Math.round(new Date().getTime() / 1000);
        if (state.tokenData) {
            return (state.token !== null && state.tokenData.exp > now)
        }
        return false
    },
    CURRENT_USER_DATA: state => {
        return state.currentUserData
    },
};

const mutations = {
    SET_TOKEN: (state, payload) => {
        state.token = payload
    },
    SET_VERIFIED_TOKEN: (state, payload) => {
        state.tokenData = payload
    },
    SET_CURRENT_USER_DATA: (state, payload) => {
        state.currentUserData = payload
    },
};

const actions = {
    async doLogin({commit}, {username, password}) {
        const response = await apolloClient.mutate({
            mutation: LOGIN_MUTATION,
            variables: {
                username: username,
                password: password
            }
        });
        commit('SET_TOKEN', response.data.tokenAuth.token)
    },

    async verifyToken({commit}) {
        const response = await apolloClient.mutate({
            mutation: VERIFY_TOKEN_MUTATION,
            variables: {
                token: this.getters.TOKEN
            }
        });
        commit('SET_VERIFIED_TOKEN', response.data.verifyToken.payload)
    },

    logout({commit}) {
        commit('SET_TOKEN', null);
        commit('SET_CURRENT_USER_DATA', null)
        // todo revoke token
    },

    async fetchUserData({commit}) {
        const response = await apolloClient.query({
            query: CURRENT_USER,
        });
        commit('SET_CURRENT_USER_DATA', response.data.me)
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
};