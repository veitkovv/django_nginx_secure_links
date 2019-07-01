import LOGIN_MUTATION from '../../graphql/TokenAuth.gql'
import VERIFY_TOKEN_MUTATION from '../../graphql/VerifyToken.gql'
import CURRENT_USER from '../../graphql/Me.gql'
import REFRESH_TOKEN from '../../graphql/RefreshToken.gql'

import {apolloClient} from '../../vue-apollo'
import Cookies from 'js-cookie'

const state = {
    token: null,
    tokenData: null,
    currentUserData: null,
    csrfToken: null,
};

const getters = {
    TOKEN: state => {
        return state.token;
    },
    TOKEN_DATA: state => {
        return state.tokenData;
    },
    CSRF_TOKEN: state => {
        return state.csrfToken;
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
        state.token = payload;
    },
    SET_VERIFIED_TOKEN: (state, payload) => {
        state.tokenData = payload
    },
    SET_CURRENT_USER_DATA: (state, payload) => {
        state.currentUserData = payload
    },
    SET_CSRF: (state, payload) => {
        state.csrfToken = payload;
    }
};

const actions = {
    async takeCSRF({commit}) {
        const url = 'http://127.0.0.1/';
        await fetch(url + 'csrf/')
            .then(response => response.json())
            .then(data => {
                commit('SET_CSRF', data.csrfToken);
            })
    },
    async doLogin({commit}, {username, password}) {
        const response = await apolloClient.mutate({
            mutation: LOGIN_MUTATION,
            variables: {
                username: username,
                password: password
            }
        });
        commit('SET_TOKEN', response.data.tokenAuth.token);
        Cookies.set('JWT-Token', response.data.tokenAuth.token)
    },

    async verifyToken({commit}) {
        const cookieStoredToken = Cookies.get('JWT-Token');
        if (cookieStoredToken !== undefined) {
            commit('SET_TOKEN', cookieStoredToken);
            const response = await apolloClient.mutate({
                mutation: VERIFY_TOKEN_MUTATION,
                variables: {
                    token: this.getters.TOKEN
                }
            });
            commit('SET_VERIFIED_TOKEN', response.data.verifyToken.payload);
        }
    },

    async refreshToken({commit}) {
        const response = await apolloClient.mutate({
            mutation: REFRESH_TOKEN,
            variables: {
                token: this.getters.TOKEN
            }
        });
        commit('SET_TOKEN', response.data.refreshToken.token);
        Cookies.set('JWT-Token', response.data.refreshToken.token);
        commit('SET_VERIFIED_TOKEN', response.data.refreshToken.payload);
    },

    async fetchUserData({commit}) {
        const response = await apolloClient.query({
            query: CURRENT_USER,
        });
        commit('SET_CURRENT_USER_DATA', response.data.me)
    },

    logout({commit}) {
        Cookies.remove('JWT-Token');
        Cookies.remove('JWT-Token-data');
        commit('SET_TOKEN', null);
        commit('SET_CURRENT_USER_DATA', null)
        // todo revoke token
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};