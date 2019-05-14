let maxToastId = 0;

function createMessage(id, text, severity, dismissAfter) {
    return {
        id,
        text,
        severity,
        dismissAfter
    }
}


const state = {
    alerts: []
};

const getters = {
    ALERTS: state => {
        return state.alerts;
    }
};

const mutations = {
    ADD_ALERT: (state, payload) => {
        state.alerts.push(payload)
    },
    REMOVE_ALERT: (state, payload) => {
        state.alerts = state.alerts.filter(m => m.id !== payload)
    }
};

const actions = {
    showAlert({commit}, {severity = 'info', text, dismissAfter = 3000}) {
        const id = ++maxToastId;
        commit('ADD_ALERT', createMessage(id, text, severity, dismissAfter));
        setTimeout(() => commit('REMOVE_ALERT', id), dismissAfter)
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};