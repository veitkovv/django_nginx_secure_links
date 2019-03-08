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

        data: () => ({
            rowsPerPageItems: [4, 8, 12],
            pagination: {
                rowsPerPage: 4
            },
            items: [
                {
                    name: 'Frozen Yogurt',
                    calories: 159,
                    fat: 6.0,
                    carbs: 24,
                    protein: 4.0,
                    sodium: 87,
                    calcium: '14%',
                    iron: '1%'
                },
                {
                    name: 'Ice cream sandwich',
                    calories: 237,
                    fat: 9.0,
                    carbs: 37,
                    protein: 4.3,
                    sodium: 129,
                    calcium: '8%',
                    iron: '1%'
                },
                {
                    name: 'Eclair',
                    calories: 262,
                    fat: 16.0,
                    carbs: 23,
                    protein: 6.0,
                    sodium: 337,
                    calcium: '6%',
                    iron: '7%'
                },
                {
                    name: 'Cupcake',
                    calories: 305,
                    fat: 3.7,
                    carbs: 67,
                    protein: 4.3,
                    sodium: 413,
                    calcium: '3%',
                    iron: '8%'
                },
                {
                    name: 'Gingerbread',
                    calories: 356,
                    fat: 16.0,
                    carbs: 49,
                    protein: 3.9,
                    sodium: 327,
                    calcium: '7%',
                    iron: '16%'
                },
                {
                    name: 'Jelly bean',
                    calories: 375,
                    fat: 0.0,
                    carbs: 94,
                    protein: 0.0,
                    sodium: 50,
                    calcium: '0%',
                    iron: '0%'
                },
                {
                    name: 'Lollipop',
                    calories: 392,
                    fat: 0.2,
                    carbs: 98,
                    protein: 0,
                    sodium: 38,
                    calcium: '0%',
                    iron: '2%'
                },
                {
                    name: 'Honeycomb',
                    calories: 408,
                    fat: 3.2,
                    carbs: 87,
                    protein: 6.5,
                    sodium: 562,
                    calcium: '0%',
                    iron: '45%'
                },
                {
                    name: 'Donut',
                    calories: 452,
                    fat: 25.0,
                    carbs: 51,
                    protein: 4.9,
                    sodium: 326,
                    calcium: '2%',
                    iron: '22%'
                },
                {
                    name: 'KitKat',
                    calories: 518,
                    fat: 26.0,
                    carbs: 65,
                    protein: 7,
                    sodium: 54,
                    calcium: '12%',
                    iron: '6%'
                }
            ]
        })
    }
</script>
