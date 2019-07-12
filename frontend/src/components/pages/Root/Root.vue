<template>
    <v-container grid-list-md ma-auto pa-0>
        <v-layout align-center justify-start column fill-height>
            <v-flex xs8 sm8>
                <v-layout align-center justify-space-between row wrap>
                    <v-flex xs12 sm6>
                        <v-text-field v-model="searchStr"
                                      append-icon="search"
                                      label="Поиск"
                                      single-line
                                      hide-details
                        ></v-text-field>
                        <span class="subheader grey--text">Всего элементов: {{EXISTING_FILES.length}}</span>

                        <div v-if="EXISTING_FILES.length === 0 && searchStr.length === 0">
                            <h3>Папка secure пуста</h3>
                        </div>
                        <div v-if="EXISTING_FILES.length === 0 && searchStr.length !== 0">
                            <h3>Поиск не дал результата</h3>
                        </div>
                    </v-flex>

                    <v-flex xs12 sm4>
                        <v-select
                                v-model="select"
                                :items="selectItems"
                                item-text="text"
                                item-value="value"
                                label="Сортировка"
                                persistent-hint
                                return-object
                                single-line
                        ></v-select>
                    </v-flex>

                    <v-flex xs12 sm2>
                        <v-switch v-model="withoutLinksOnly" label="Без ссылок"></v-switch>
                    </v-flex>

                </v-layout>

                <template v-for="(item, index) in EXISTING_FILES">
                    <file-component :file="item" :key="index"></file-component>
                </template>
            </v-flex>
        </v-layout>

    </v-container>
</template>

<script>
    import {mapGetters, mapActions} from 'vuex';
    import FileComponent from './FileComponent';

    export default {
        name: "FileListRoot",
        components: {FileComponent},

        data() {
            return {
                select: {text: "По алфавиту по возрастанию", value: 'ab-asc'},
                selectItems: [
                    {text: "По алфавиту вниз", value: 'ab-asc'},
                    {text: "По алфавиту вверх", value: 'ab-desc'},
                    {text: "Сначала старые", value: 'created-asc'},
                    {text: "Сначала новые", value: 'created-desc'},

                ],
                searchStr: '',
                withoutLinksOnly: false,
                // TODO https://github.com/apollographql/react-apollo/issues/1314 loading always false bug
            }
        },
        computed: {
            ...mapGetters([
                'EXISTING_FILES',
                'EXISTING_FS',
                'WITHOUT_LINKS_ONLY'
            ]),
        },
        methods: {
            ...mapActions(['fetchFileList', 'changeWithoutLinksOnly'])
        },
        watch: {
            searchStr: function (val) {
                this.fetchFileList({
                    searchStr: val,
                    orderBy: this.select,
                    withoutLinksOnly: this.WITHOUT_LINKS_ONLY
                })
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            },
            select: function (select) {
                this.fetchFileList({
                    orderBy: select.value,
                    searchStr: this.searchStr,
                    withoutLinksOnly: this.WITHOUT_LINKS_ONLY
                })
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            },
            withoutLinksOnly: function () {
                this.changeWithoutLinksOnly().then(() => {
                    this.fetchFileList({
                        orderBy: this.select,
                        searchStr: this.searchStr,
                        withoutLinksOnly: this.WITHOUT_LINKS_ONLY
                    })
                        .then(() => console.log('Список файлов успешно загружен с сервера'))
                        .catch(err => this.showSnackbar({
                            text: err,
                            color: 'error'
                        }))
                })
            }
        },
        mounted() {
            this.fetchFileList().then(() =>
                console.log('Список файлов успешно загружен с сервера')
            )
        }
    }
</script>

