<template>
    <v-flex xs12 sm6 offset-sm3>
        <v-card>
            <v-list two-line subheader>
                <v-subheader inset>Файлы</v-subheader>
                <template v-for="(item, index) in items">
                    <v-list-tile
                            :key="item.title"
                            avatar
                            @click=""
                    >
                        <v-list-tile-avatar>
                            <v-icon :class="[item.iconClass]">{{ item.icon }}</v-icon>
                        </v-list-tile-avatar>

                        <v-list-tile-content>
                            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
                            <v-list-tile-sub-title class="text--primary">{{ item.subtitle }}</v-list-tile-sub-title>
                            <v-list-tile-sub-title>{{ item.subtitle }}</v-list-tile-sub-title>
                        </v-list-tile-content>
                        <v-list-tile-action>
                            <v-list-tile-action-text>bla</v-list-tile-action-text>
                        </v-list-tile-action>
                    </v-list-tile>
                    <v-divider
                            v-if="index + 1 < items.length"
                            :key="index"
                    ></v-divider>
                </template>
            </v-list>
        </v-card>
    </v-flex>
</template>

<script>
    import FileListMenu from "./FileListMenu";

    export default {
        name: "FileList",
        components: {FileListMenu},
        data() {
            return {
                items: [
                    {icon: 'folder', iconClass: 'grey lighten-1 white--text', title: 'Photos', subtitle: 'Jan 9, 2014'},
                    {
                        icon: 'folder',
                        iconClass: 'grey lighten-1 white--text',
                        title: 'Recipes',
                        subtitle: 'Jan 17, 2014'
                    },
                    {icon: 'folder', iconClass: 'grey lighten-1 white--text', title: 'Work', subtitle: 'Jan 28, 2014'},
                    {
                        icon: 'assignment',
                        iconClass: 'blue white--text',
                        title: 'Vacation itinerary',
                        subtitle: 'Jan 20, 2014'
                    },
                    {
                        icon: 'call_to_action',
                        iconClass: 'amber white--text',
                        title: 'Kitchen remodel',
                        subtitle: 'Jan 10, 2014'
                    }
                ],
                headers: [
                    {
                        text: 'Имя файла',
                        align: 'left',
                        sortable: false,
                        value: 'filename',
                        width: '60%'
                    },
                    {text: 'Размер', value: 'size'},
                    {text: 'Дата создания файла', value: 'created_at'},
                    {
                        text: 'Дейтсвия',
                        value: 'actions',
                        sortable: false,
                        width: '10%'
                    },
                ],

                files: [
                    {
                        filename: '1',
                        size: 2,
                        created_at: 3,
                        secure_link: {
                            available: false,
                        }
                    },
                    {
                        filename: '2',
                        size: 3,
                        created_at: 4,
                        secure_link: {
                            available: true,
                            url: 'http://123',
                            expires: 11111
                        }
                    }
                ],
                valueDeterminate: 40
            }
        },

        methods: {}
    }
</script>

<style scoped>

</style>