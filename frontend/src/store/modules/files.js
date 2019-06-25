import {apolloClient} from '../../vue-apollo'
import FILES_QUERY from '../../graphql/Files.gql'

const state = {
    files: [],
};

const getters = {
    FILES: state => {
        return state.files;
    },
    // backend contains deleted files too. for history. so filter it
    EXISTING_FILES: state => {
        return state.files.filter(item => item.exists)
        // return state.files.filter(item => item.exists & !item.isFolder)
    },

    EXISTING_FS: state => {
        return state.files.filter(item => item.exists)
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
    async getFiles({commit}, search = '') {
        const response = await apolloClient.query({
            query: FILES_QUERY,
            variables: {
                search: search
            }
        });
        commit('SET_FILES', response.data.allFiles)
    },
};

export default {
    state,
    getters,
    mutations,
    actions,
};