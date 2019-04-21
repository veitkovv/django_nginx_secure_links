<template>
    <v-data-table
            :headers="headers"
            :items="files"
            class="elevation-1"
    >
        <template v-slot:items="props">
            <td>{{ props.item.filename }}</td>
            <td>{{ props.item.size }}</td>
            <td>{{ props.item.created_at }}</td>
            <td class="justify-center">
                <v-layout align-center justify-start row fill-height>
                    <file-list-menu :item="props.item"/>
                    <v-tooltip bottom>
                        <template v-slot:activator="{ on }">
                            <v-icon color="red darken-2" class="mr-2" v-on="on" @click="">delete</v-icon>
                        </template>
                        <span>Удалить файл</span>
                    </v-tooltip>
                </v-layout>
            </td>
        </template>
    </v-data-table>
</template>

<script>
    import FileListMenu from "./FileListMenu";

    export default {
        name: "FileList",
        components: {FileListMenu},
        data() {
            return {
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