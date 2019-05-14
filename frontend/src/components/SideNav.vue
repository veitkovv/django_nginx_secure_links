<template>
    <v-navigation-drawer
            fixed
            :value="SIDENAV_DRAWER"
            app
    >
        <v-list dense>
            <v-list-tile :to="{path: '/'}">
                <v-list-tile-action>
                    <v-icon>home</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>Главная</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>

            <v-list-tile :to="{path: '/login'}">
                <v-list-tile-action>
                    <v-icon>exit_to_app</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>Авторизация</v-list-tile-title>
                </v-list-tile-content>
            </v-list-tile>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "SideNav",
        data: () => ({}),
        computed: {
            ...mapGetters(['SIDENAV_DRAWER']),
        }
    }
</script>
