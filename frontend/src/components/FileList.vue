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
            <td>
                <div v-if="props.item.secure_link.available">
                    <v-btn color="success" block>Скопировать ссылку
                        <v-icon right dark>public</v-icon>
                    </v-btn>
                    <v-btn color="primary" block>Пересоздать ссылку
                        <v-icon right dark>file_copy</v-icon>
                    </v-btn>
                    <v-progress-linear v-model="valueDeterminate"></v-progress-linear>
                </div>
                <div v-else>
                    <v-btn color="primary" block>Создать ссылку
                        <v-icon right dark>cloud_upload</v-icon>
                    </v-btn>
                </div>
            </td>
        </template>
    </v-data-table>
</template>

<script>
    export default {
        name: "FileList",
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
        }
    }
</script>

<style scoped>

</style>