<template>
    <v-navigation-drawer
            fixed
            :value="SIDENAV_DRAWER"
            app
    >
        <v-list dense
                v-for="route in routes"
        >
            <v-list-tile :to="route.path">
                <v-list-tile-action>
                    <v-icon>{{route.icon}}</v-icon>
                </v-list-tile-action>
                <v-list-tile-content>
                    <v-list-tile-title>{{route.name}}</v-list-tile-title>
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
            routes: function () {
                //Last one is default route
                return this.$router.options.routes.slice(0, -1)
            }
        }
    }
</script>
