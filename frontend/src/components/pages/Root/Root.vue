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
                                v-model="orderBy"
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
    import {mapGetters, mapActions, mapMutations} from 'vuex';
    import FileComponent from './FileComponent';

    export default {
        name: "FileListRoot",
        components: {FileComponent},

        data() {
            return {
                selectItems: [
                    {text: "По алфавиту вниз", value: 'ab-asc'},
                    {text: "По алфавиту вверх", value: 'ab-desc'},
                    {text: "Сначала старые", value: 'created-asc'},
                    {text: "Сначала новые", value: 'created-desc'},

                ],
            }
        },
        computed: {
            ...mapGetters([
                'EXISTING_FILES',
                'EXISTING_FS',
                'WITHOUT_LINKS_ONLY',
                'ORDER_BY',
                'SEARCH_STR',
            ]),
            orderBy: {
                get() {
                    return this.ORDER_BY
                },
                set(val) {
                    this.SET_ORDER_BY(val);
                }
            },
            searchStr: {
                get() {
                    return this.SEARCH_STR
                },
                set(val) {
                    this.SET_SEARCH_STR(val)
                }
            },
            withoutLinksOnly: {
                get() {
                    return this.WITHOUT_LINKS_ONLY
                },
                set() {
                    this.changeWithoutLinksOnly()
                }
            }
        },
        methods: {
            ...mapActions(['fetchFileList', 'changeWithoutLinksOnly']),
            ...mapMutations(['SET_ORDER_BY', 'SET_SEARCH_STR'])
        },
        watch: {
            searchStr: function () {
                this.fetchFileList()
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            },
            orderBy: function () {
                this.fetchFileList()
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            },
            withoutLinksOnly: function () {
                this.fetchFileList()
                    .then(() => console.log('Список файлов успешно загружен с сервера'))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            }
        },
        mounted() {
            this.fetchFileList().then(() =>
                console.log('Список файлов успешно загружен с сервера')
            )
        }
    }
</script>

