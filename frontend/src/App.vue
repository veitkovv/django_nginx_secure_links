<template>
    <v-app id="inspire">
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
            <v-layout align-center>
                <a class="subheading" href="mailto:it@yamal-region.tv">Задавайте вопросы по электронной почте</a>
            </v-layout>
            <span class="mr-4">ver. 1.1</span>
            <div>&copy; {{ new Date().getFullYear() }} by Veytko V.V.</div>
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
                    this.fetchDefaultSettings();
                    this.fetchUserData();
                });
            });
        },
        created() {
            document.title = 'Public Secure Links';
        }
    }
</script>

<style scoped>
    .a {
        text-decoration: none;
    }
</style>