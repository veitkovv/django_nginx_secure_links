<template>
    <v-flex xs12 sm7 offset-sm2>
        <v-text-field v-model="search"
                      append-icon="search"
                      label="Поиск"
                      single-line
                      hide-details
        ></v-text-field>

        <span class="subheader grey--text">Всего элементов: {{EXISTING_FILES.length}}</span>
        <div v-if="EXISTING_FILES.length === 0 && search.length === 0">
            <h3>Папка secure пуста</h3>
        </div>
        <div v-if="EXISTING_FILES.length === 0 && search.length !== 0">
            <h3>Поиск не дал результата</h3>
        </div>

        <template v-for="(item, index) in EXISTING_FILES">
            <file-component :file="item" :key="index"></file-component>
        </template>


    </v-flex>
</template>

<script>
    import {mapGetters, mapActions} from 'vuex';
    import FileComponent from './FileComponent';

    export default {
        name: "FileListRoot",
        components: {FileComponent},

        data() {
            return {
                valueDeterminate: 40,
                search: '',
                // TODO https://github.com/apollographql/react-apollo/issues/1314 loading always false bug
            }
        },
        computed: {
            ...mapGetters([
                'EXISTING_FILES',
                'EXISTING_FS',
            ]),
        },
        methods: {
            ...mapActions(['getFiles'])
        },
        watch: {
            search: function (val) {
                this.getFiles(val)
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            }
        },
        mounted() {
            this.getFiles().then(() =>
                console.log('Список файлов успешно загружен с сервера')
            )
        }
    }
</script>
