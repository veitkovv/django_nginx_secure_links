<template>
    <div id="app">
        <v-app id="inspire">
            <v-toolbar scroll-toolbar-off-screen color="primary" dark fixed prominent app>
                <v-toolbar-side-icon></v-toolbar-side-icon>
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
                    <v-btn icon>
                        <v-icon>refresh</v-icon>
                    </v-btn>
                    <v-btn icon>
                        <v-icon>exit_to_app</v-icon>
                    </v-btn>
                </v-toolbar-items>
            </v-toolbar>
            <main>
                <v-content>
                    <file-list></file-list>
                </v-content>
            </main>
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


    }
</script>
