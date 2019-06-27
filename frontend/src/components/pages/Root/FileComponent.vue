<template>
    <v-card>
        <v-card-title primary-title>
            <v-list-tile-avatar color="grey darken-3">
                <v-icon class="grey white--text">{{ file.fileType }}</v-icon>
            </v-list-tile-avatar>
            <div>
                <div class="title">{{ file.filename }}</div>
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
                                <li> Размер: {{humanFileSize(file.size, true)}}</li>
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
                                    color="success"
                                    flat
                                    v-clipboard:copy="secureLink.url"
                                    v-clipboard:success="clipboardSuccessHandler"
                                    v-clipboard:error="clipboardErrorHandler"
                                    @click="dialog = false"
                            >
                                Скопировать
                            </v-btn>
                        </v-card-actions>
                    </v-card>

                </v-dialog>

                <v-btn icon @click.native="show = !show" disabled>
                    <v-icon>{{ show ? 'keyboard_arrow_up' : 'keyboard_arrow_down' }}</v-icon>
                </v-btn>

                <v-list-tile-action>
                    <v-list-tile-action-text>
                        {{humanFileSize(file.size, true)}}
                    </v-list-tile-action-text>
                </v-list-tile-action>

            </v-card-actions>
        </v-card-title>

        <v-slide-y-transition>
            <!--То что в дропдауне-->
            <v-card-text v-show="show">
                <v-layout row wrap>
                    <v-flex xs8>
                        <div v-if="file.isFolder">
                            <span>Папка содержит файлы: </span>
                        </div>
                    </v-flex>
                    <v-flex xs4>

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
            secureLink: {
                url: '',
                expires: ''
            },
            loading: false,
        }),
        computed: {
            linkDeadlineTime: function () {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(this.secureLink.expires);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            }
        },
        methods: {
            ...mapMutations(['showSnackbar']),
            ...mapActions(['getFiles']),
            dateModified(timestamp) {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(timestamp * 1000);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            },
            humanFileSize(bytes, si) {
                let thresh = si ? 1000 : 1024;
                if (Math.abs(bytes) < thresh) {
                    return bytes + ' B';
                }
                let units = si
                    ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB']
                    : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
                let u = -1;
                do {
                    bytes /= thresh;
                    ++u;
                } while (Math.abs(bytes) >= thresh && u < units.length - 1);
                return bytes.toFixed(1) + ' ' + units[u];
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
                });
            },
            createFolderLink(file) {
                this.loading = true;
                if (file.tarballCreated) {
                    console.log('tarball created')
                } else {
                    this.$apollo.mutate({
                        mutation: CREATE_ARCHIVE,
                        variables: {
                            folderName: file.filename
                        },
                    }).then((data) => {
                        this.createLink(data.data.createArchive.createdArchiveName)
                    });
                }
            },
            clipboardSuccessHandler({value, event}) {
                this.showSnackbar({
                    text: 'Ссылка успешно скопирована'
                })
            },

            clipboardErrorHandler({value, event}) {
                this.showSnackbar({
                    text: 'Ссылка не скопирована',
                    color: 'error'
                })
            }
        }
    }
</script>
