import ApolloClient from 'apollo-boost'
// https://lmiller1990.github.io/electic/posts/integrating_apollo_with_vue_and_vuex.html
export default new ApolloClient({
    uri: 'http://127.0.0.1:8000/graphql/'
})