<template>
    <v-card>
        <v-card-title primary-title>
            <v-avatar class="mr-3">
                <v-icon class="grey white--text">{{ fileIcon[file.fileType] }}</v-icon>
            </v-avatar>
            <div>
                <div class="title text-overflow">{{ file.filename }}</div>
                <span class="grey--text">Изменено: {{dateModified(file.modified) }}</span>
            </div>
            <v-spacer></v-spacer>
            <v-card-actions>
                <v-dialog
                        v-model="dialog"
                        width="500"
                >
                    <template v-slot:activator="{ on }">
                        <!--Если папка-->
                        <div v-if="file.isFolder">
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on }">
                                    <v-btn
                                            :disabled="file.isOversize"
                                            color="primary"
                                            outline
                                            :loading="loading"
                                            v-on="on"
                                            @click.native="createFolderLink(file)"
                                    >
                                        Создать ссылку
                                    </v-btn>
                                </template>
                                <span>Сервер создаст ссылку на архив без сжатия, это займет некоторое время</span>
                            </v-tooltip>
                        </div>

                        <!--Если файл-->
                        <v-btn v-else
                               color="primary"
                               outline
                               :loading="loading"
                               @click.native="createLink(file.filename)"
                        >
                            Создать ссылку
                        </v-btn>

                    </template>

                    <!--Содержимое диалога-->
                    <v-card>
                        <v-card-title
                                class="headline grey lighten-2"
                                primary-title
                        >
                            Ссылка успешно создана
                        </v-card-title>
                        <v-card-text>
                            <ul>
                                <li> Файл: {{file.filename}}</li>
                                <li> Размер: {{file.size}}</li>
                                <li> Ссылка действительна до: {{linkDeadlineTime}}</li>
                            </ul>
                        </v-card-text>

                        <v-card-actions>
                            <v-spacer></v-spacer>

                            <v-btn
                                    color="primary"
                                    flat
                                    @click="dialog = false"
                            >
                                Отмена
                            </v-btn>

                            <v-btn
                                    color="secondary"
                                    flat
                                    v-clipboard:copy="secureLink.url"
                                    v-clipboard:success="clipboardSuccessHandler"
                                    v-clipboard:error="clipboardErrorHandler"
                                    @click="dialog = false"
                            >
                                Скопировать ссылку
                            </v-btn>

                            <v-btn
                                    color="success"
                                    flat
                                    v-clipboard:copy="humanAnswer"
                                    v-clipboard:success="clipboardSuccessHandler"
                                    v-clipboard:error="clipboardErrorHandler"
                                    @click="dialog = false"
                            >
                                Скопировать ответ
                            </v-btn>
                        </v-card-actions>
                    </v-card>

                </v-dialog>

                <v-btn icon @click.native="show = !show">
                    <v-icon>{{ show ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</v-icon>
                </v-btn>

                <v-list-tile-action>
                    <v-list-tile-action-text>
                        {{file.size}}
                    </v-list-tile-action-text>
                </v-list-tile-action>

            </v-card-actions>
        </v-card-title>

        <v-slide-y-transition>
            <!--То что в дропдауне-->
            <v-card-text v-show="show">
                <v-layout row wrap>
                    <v-flex xs6>
                        {{file.directoryIsBig}}
                        <span>Полное имя файла: "{{file.filename}}"</span>
                    </v-flex>
                    <v-flex xs4>
                        <div v-if="file.isOversize">
                            <v-tooltip bottom>
                                <template v-slot:activator="{ on }">
                                    <v-btn
                                            :disabled="file.directoryIsBig"
                                            color="primary"
                                            outline
                                            :loading="loading"
                                            v-on="on"
                                            @click.native="createFolderLink(file)"
                                    >
                                        Папка очень большая, создать ссылку?
                                    </v-btn>
                                </template>
                                <span>Сервер создаст ссылку на архив без сжатия, это займет некоторое время</span>
                            </v-tooltip>
                        </div>
                    </v-flex>
                </v-layout>

            </v-card-text>
        </v-slide-y-transition>
        <v-divider></v-divider>
    </v-card>

</template>

<script>
    import CREATE_SECURE_LINK from '../../../graphql/CreateSecureLink.gql'
    import CREATE_ARCHIVE from '../../../graphql/CreateArchive.gql'
    import {mapActions, mapMutations} from 'vuex'

    export default {
        name: "FileComponent",
        props: {
            file: Object
        },
        data: () => ({
            show: false,
            dialog: false,
            loading: false,
            tarCreatedDialog: false,
            secureLink: {
                url: '',
                expires: ''
            },
            fileIcon: {
                'image': 'image',
                'document': 'file_copy',
                'video': 'local_movies',
                'audio': 'audiotrack',
                'archive': 'archive',
                'folder': 'folder',
                'undefined': 'block'
            }
        }),
        computed: {
            linkDeadlineTime: function () {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(this.secureLink.expires);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            },
            humanAnswer: function () {
                return [
                    'Создана ссылка на файл',
                    '',
                    ' - Файл: ' + this.file.filename + '',
                    ' - Размер: ' + this.file.size,
                    ' - Ссылка действительна до: ' + this.linkDeadlineTime,
                    ' - URL: ' + this.secureLink.url,
                ].join("\n");
            }
        }
        ,
        methods: {
            ...mapMutations(['showSnackbar']),
            ...mapActions(['fetchFileList']),
            dateModified(timestamp) {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(timestamp * 1000);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            },
            createLink(filename) {
                this.secureLink.url = '';
                this.secureLink.expires = 0;
                this.loading = true;

                this.$apollo.mutate({
                    mutation: CREATE_SECURE_LINK,
                    variables: {
                        filename: filename
                    },
                }).then((data) => {
                    this.secureLink.url = data.data.createSecureLink.secureLink;
                    this.secureLink.expires = data.data.createSecureLink.linkDeadline;
                    this.dialog = true;
                    this.loading = false;
                }).catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }
                ));
            }
            ,
            createFolderLink(file) {
                this.loading = true;
                if (file.tarballCreated) {
                    this.showSnackbar({
                        text: 'Архив данной папки уже создан, создайте ссылку на него.',
                        color: 'info'

                    });
                    this.loading = false;
                } else {
                    this.$apollo.mutate({
                        mutation: CREATE_ARCHIVE,
                        variables: {
                            folderName: file.filename
                        },
                    }).then((data) => {
                        this.createLink(data.data.createArchive.createdArchiveName)
                    }).catch(err => this.showSnackbar({
                            text: err,
                            color: 'error'
                        }
                    ));
                }
            }
            ,
            clipboardSuccessHandler({value, event}) {
                this.showSnackbar({
                    text: 'Копирование успешно'
                })
            }
            ,

            clipboardErrorHandler({value, event}) {
                this.showSnackbar({
                    text: 'Ошибка копирования',
                    color: 'error'
                })
            },
        }
    }
</script>

<style>
    .text-overflow {
        width: 500px;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
    }

    @media (max-width: 1000px) {
        .text-overflow {
            width: 200px;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
    }
</style>