import LOGIN_MUTATION from '../../graphql/TokenAuth.gql'
import VERIFY_TOKEN_MUTATION from '../../graphql/VerifyToken.gql'
import CURRENT_USER from '../../graphql/Me.gql'
import REFRESH_TOKEN from '../../graphql/RefreshToken.gql'
import REVOKE_TOKEN from '../../graphql/RevokeToken.gql'
import API_SERVER from '../../../apiServer'

import {apolloClient} from '../../vue-apollo'
import Cookies from 'js-cookie'

const state = {
    tokenAuth: {
        token: '',
        refreshToken: '',
    },
    tokenData: '',
    currentUserData: '',
    csrfToken: '',
};

const getters = {
    TOKEN_AUTH: state => {
        return state.tokenAuth;
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
    FULLNAME: state => {
        if (state.currentUserData !== null) {
            return state.currentUserData.firstName + ' ' + state.currentUserData.lastName
        }
    }
};

const mutations = {
    SET_TOKEN_AUTH: (state, {token, refreshToken}) => {
        state.tokenAuth.token = token;
        state.tokenAuth.refreshToken = refreshToken;
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
        await fetch(API_SERVER + '/csrf/')
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
        commit('SET_TOKEN_AUTH', response.data.tokenAuth);
        Cookies.set('JWT-Token', state.tokenAuth)
    },

    async verifyToken({commit}) {
        let cookieStoredToken = Cookies.get('JWT-Token');
        if (cookieStoredToken) {
            cookieStoredToken = JSON.parse(cookieStoredToken);
            commit('SET_TOKEN_AUTH', {token: cookieStoredToken.token, refreshToken: cookieStoredToken.refreshToken});
            const response = await apolloClient.mutate({
                mutation: VERIFY_TOKEN_MUTATION,
                variables: {
                    token: state.tokenAuth.token
                }
            });
            commit('SET_VERIFIED_TOKEN', response.data.verifyToken.payload);
        }
    },

    async refreshToken({commit}) {
        const response = await apolloClient.mutate({
            mutation: REFRESH_TOKEN,
            variables: {
                token: this.getters.TOKEN_AUTH.refreshToken
            }
        });
        commit('SET_TOKEN_AUTH', {
            token: response.data.refreshToken.token,
            refreshToken: response.data.refreshToken.refreshToken
        });
        commit('SET_VERIFIED_TOKEN', response.data.refreshToken.payload);
        Cookies.set('JWT-Token', response.data.refreshToken);
    },

    async revokeToken({commit}) {
        await apolloClient.mutate({
            mutation: REVOKE_TOKEN,
            variables: {
                refreshToken: state.tokenAuth.refreshToken
            }
        });
        commit('SET_TOKEN_AUTH', {token: '', refreshToken: ''});
        commit('SET_CURRENT_USER_DATA', '');
        commit('SET_VERIFIED_TOKEN', '');
        Cookies.remove('JWT-Token');

    },

    async fetchUserData({commit}) {
        const response = await apolloClient.query({
            query: CURRENT_USER,
        });
        commit('SET_CURRENT_USER_DATA', response.data.me)
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};