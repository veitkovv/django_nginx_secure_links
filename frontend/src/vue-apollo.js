import Vue from 'vue'
import {ApolloClient} from 'apollo-client'
import {HttpLink} from 'apollo-link-http'
import {InMemoryCache} from 'apollo-cache-inmemory'
import VueApollo from 'vue-apollo'

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
}

const httpLink = new HttpLink({
    // You should use an absolute URL here
    uri: 'http://127.0.0.1:8000/graphql/',
})
// Create the apollo client
export const apolloClient = new ApolloClient({
    link: httpLink,
    cache: new InMemoryCache(),
    connectToDevTools: true,
    defaultOptions: defaultOptions
})
const apolloProvider = new VueApollo({
    defaultClient: apolloClient,
})
// Install the vue plugin
Vue.use(VueApollo)

export default apolloProvider

