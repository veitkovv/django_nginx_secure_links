<template>
    <div id="app">
        <v-app id="inspire">
            <v-navigation-drawer
                    fixed
                    v-model="drawer"
                    app
            >
                <v-list dense>
                    <v-list-tile @click="">
                        <v-list-tile-action>
                            <v-icon>home</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Home</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                    <v-list-tile @click="">
                        <v-list-tile-action>
                            <v-icon>contact_mail</v-icon>
                        </v-list-tile-action>
                        <v-list-tile-content>
                            <v-list-tile-title>Contact</v-list-tile-title>
                        </v-list-tile-content>
                    </v-list-tile>
                </v-list>
            </v-navigation-drawer>
            <v-toolbar scroll-toolbar-off-screen color="primary" dark fixed prominent app>
                <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
                <v-spacer></v-spacer>
                <v-flex xs12 md4 text-xs-center>
                    <v-text-field v-model="search"
                                  append-icon="search"
                                  label="Поиск"
                                  single-line
                                  hide-details
                                  color="secondary"
                    ></v-text-field>
                </v-flex>
                <v-spacer></v-spacer>
                <v-toolbar-items class="hidden-sm-and-down">
                    <v-btn icon @click="$store.dispatch('getFiles')">
                        <v-icon>refresh</v-icon>
                    </v-btn>
                    <v-btn icon>
                        <v-icon>exit_to_app</v-icon>
                    </v-btn>
                </v-toolbar-items>
            </v-toolbar>
            <main>
                <v-content>
                    <file-list :search="search"></file-list>
                </v-content>
            </main>
            <v-footer class="pa-3">
                <v-spacer></v-spacer>
                <div>&copy; {{ new Date().getFullYear() }}</div>
            </v-footer>
        </v-app>
    </div>
</template>

<script>
    import FileList from '../src/components/FileList'

    export default {
        name: 'App',
        components: {
            FileList,
        },
        data: () => ({
            drawer: null,
            search: '',
        })

    }
</script>
