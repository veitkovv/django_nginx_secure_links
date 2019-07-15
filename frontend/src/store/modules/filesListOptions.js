const state = {
    withoutLinksOnly: false,
    orderBy: {text: "По алфавиту по возрастанию", value: 'ab-asc'},
    searchStr: ''
};

const getters = {
    WITHOUT_LINKS_ONLY: state => {
        return state.withoutLinksOnly
    },
    ORDER_BY: state => {
        return state.orderBy
    },
    SEARCH_STR: state => {
        return state.searchStr
    }
};

const mutations = {
    CHANGE_WITHOUT_LINKS_ONLY: (state, payload) => {
        state.withoutLinksOnly = payload
    },
    SET_ORDER_BY: (state, payload) => {
        state.orderBy = payload
    },
    SET_SEARCH_STR: (state, payload) => {
        state.searchStr = payload
    }
};

const actions = {};

export default {
    state,
    getters,
    mutations,
    actions,
};