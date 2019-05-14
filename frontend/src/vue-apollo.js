import Vue from 'vue'
import {ApolloClient} from 'apollo-client'
import {ApolloLink, concat, split} from 'apollo-link';
import {HttpLink} from 'apollo-link-http'
import {InMemoryCache} from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'
import {store} from '../store/index'

//https://stackoverflow.com/questions/47879016/how-to-disable-cache-in-apollo-link-or-apollo-client
const defaultOptions = {
    watchQuery: {
        fetchPolicy: 'network-only',
        errorPolicy: 'ignore',
    },
    query: {
        fetchPolicy: 'network-only',
        errorPolicy: 'all',
    },
};

const httpLink = new HttpLink({
    // You should use an absolute URL here
    uri: 'http://127.0.0.1:8000/graphql/',
});

// https://github.com/Akryum/vue-apollo/issues/144
const authMiddleware = new ApolloLink((operation, forward) => {
    // add the authorization to the headers
    operation.setContext({
        headers: {
            // https://www.howtographql.com/graphql-python/4-authentication/
            authorization: 'JWT ' + store.getters.TOKEN,
        }
    });
    return forward(operation);
});

// Create the apollo client
export const apolloClient = new ApolloClient({
    link: concat(authMiddleware, httpLink),
    cache: new InMemoryCache(),
    connectToDevTools: true,
    defaultOptions: defaultOptions
});

const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
});

// Install the vue plugin
Vue.use(VueApollo);

export default apolloProvider

