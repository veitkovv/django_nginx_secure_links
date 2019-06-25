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
    alerts: [],
    snackbar: {
        visible: false,
        text: null,
        timeout: 3000,
        multiline: false,
        color: ''
    }
};

const getters = {
    ALERTS: state => {
        return state.alerts;
    },
    SNACKBAR: state => {
        return state.snackbar;
    }
};

const mutations = {
    ADD_ALERT: (state, payload) => {
        state.alerts.push(payload)
    },
    REMOVE_ALERT: (state, payload) => {
        state.alerts = state.alerts.filter(m => m.id !== payload)
    },
    showSnackbar(state, payload) {
        state.snackbar.text = payload.text;
        state.snackbar.multiline = (payload.text.length > 50);

        if (payload.multiline) {
            state.snackbar.multiline = payload.multiline
        }

        if (payload.timeout) {
            state.snackbar.timeout = payload.timeout
        }

        if (payload.color) {
            state.snackbar.color = payload.color
        }

        state.snackbar.visible = true
    },
    closeSnackbar(state) {
        state.snackbar.visible = false;
        state.snackbar.multiline = false;
        state.snackbar.timeout = 3000;
        state.snackbar.text = null;
        state.snackbar.color = '';
    },
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