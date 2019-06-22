<template>
    <v-app>
        <side-nav v-if="IS_AUTHENTICATED"></side-nav>
        <app-toolbar v-if="IS_AUTHENTICATED"></app-toolbar>
        <v-content>
            <v-progress-linear v-if="loading" :indeterminate="true"></v-progress-linear>

            <v-container fluid>
                <main>
                    <alerts></alerts>
                    <router-view></router-view>
                </main>
            </v-container>
        </v-content>
        <v-footer class="pa-3">
            <v-spacer></v-spacer>
            <div>&copy; {{ new Date().getFullYear() }}</div>
        </v-footer>
    </v-app>
</template>

<script>
    import {mapGetters} from 'vuex';

    import SideNav from './components/layout/SideNav'
    import AppToolbar from './components/layout/AppToolbar'
    import Alerts from '../src/components/Alerts'

    export default {
        name: 'App',
        components: {
            AppToolbar,
            SideNav,
            Alerts
        },
        data: () => ({
            loading: 0
        }),
        methods: {},
        computed: {
            ...mapGetters(['IS_AUTHENTICATED'])
        },
        mounted() {
            this.$store.dispatch('fetchDefaultSettings')
        }

    }
</script>
