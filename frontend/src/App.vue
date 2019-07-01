<template>
    <v-app>
        <side-nav v-if="IS_AUTHENTICATED"></side-nav>
        <app-toolbar v-if="IS_AUTHENTICATED"></app-toolbar>
        <v-content>
            <v-progress-linear v-if="loading" :indeterminate="true"></v-progress-linear>
            <snackbar></snackbar>
            <v-container fluid>
                <v-slide-y-transition mode="out-in">
                    <router-view></router-view>
                </v-slide-y-transition>
            </v-container>
        </v-content>

        <v-footer class="pa-3">
            <v-spacer></v-spacer>
            <div>&copy; {{ new Date().getFullYear() }}</div>
        </v-footer>
    </v-app>
</template>

<script>
    import {mapGetters, mapActions} from 'vuex';

    import SideNav from './components/layout/SideNav'
    import AppToolbar from './components/layout/AppToolbar'
    import Snackbar from './components/Snackbar'

    export default {
        name: 'App',
        components: {
            AppToolbar,
            SideNav,
            Snackbar,
        },
        data: () => ({
            loading: 0,
        }),
        methods: {
            ...mapActions([
                'fetchDefaultSettings',
                'verifyToken',
                'fetchUserData',
                'takeCSRF'
            ]),

        }
        ,
        computed: {
            ...mapGetters([
                'IS_AUTHENTICATED',
                'CSRF_TOKEN',
            ])
        }
        ,
        mounted() {
            this.takeCSRF().then(() => {
                this.verifyToken().then(() => {
                    this.fetchUserData();
                    this.fetchDefaultSettings();
                });
            });
        }
    }
</script>

<style scoped>

</style>