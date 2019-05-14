<template>
    <div id="app">
        <v-app id="inspire">
            <v-content>
                <side-nav v-if="IS_AUTHENTICATED"></side-nav>
                <app-toolbar v-if="IS_AUTHENTICATED"></app-toolbar>
                <main>
                    <alerts></alerts>
                    <router-view></router-view>
                </main>

                <v-footer class="pa-3">
                    <v-spacer></v-spacer>
                    <div>&copy; {{ new Date().getFullYear() }}</div>
                </v-footer>
            </v-content>
        </v-app>
    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    import FileList from '../src/components/FileList'
    import SideNav from './components/SideNav'
    import AppToolbar from '../src/components/AppToolbar'
    import Alerts from '../src/components/Alerts'

    export default {
        name: 'App',
        components: {
            AppToolbar,
            SideNav,
            FileList,
            Alerts
        },
        data: () => ({}),
        methods: {},
        computed: {
            ...mapGetters(['IS_AUTHENTICATED'])
        }

    }
</script>
