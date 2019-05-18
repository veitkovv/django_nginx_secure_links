<template>
    <v-menu
            v-model="menu"
            :close-on-content-click="false"
            :nudge-width="200"
            offset-x
    >

        <template v-slot:activator="{ on }">
            <v-icon color="primary" v-on="on" class="mr-2" @click="">more_vert</v-icon>
        </template>

        <v-card>
            <v-list>
                <v-list-tile v-if="item.url">
                    <v-list-tile-title>Ссылка действительна до:</v-list-tile-title>
                    <v-list-tile-action>
                        <v-btn flat color="green">Скопировать ссылку</v-btn>
                    </v-list-tile-action>
                </v-list-tile>
                <v-list-tile v-else>
                    <v-list-tile-action>
                        <v-btn dark flat color="primary">Создать ссылку</v-btn>
                    </v-list-tile-action>
                </v-list-tile>
            </v-list>
        </v-card>
    </v-menu>
</template>

<script>
    export default {
        name: "FileListMenu",
        props: {
            'item': Object,
        },
        data: () => ({
            fav: true,
            menu: false,
            message: false,
            hints: true
        }),
        computed: {}
    }
</script>

