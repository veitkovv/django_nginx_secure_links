<template>
    <v-card>
        <v-card-title primary-title>
            <v-avatar class="mr-3">
                <v-badge color="green" overlap>
                    <template v-if="file.secureLinksCreated.length === 0" v-slot:badge>
                        <v-icon
                                dark
                                small
                        >
                            star
                        </v-icon>
                    </template>
                    <v-icon
                            large
                            color="grey"
                    >
                        {{ fileIcon[file.fileType] }}
                    </v-icon>
                </v-badge>
            </v-avatar>
            <div>
                <p class="title text-overflow pl-2">{{ file.filename }}</p>
                <span class="grey--text">Изменено: {{dateModified(file.modified) }}</span>
            </div>
            <v-spacer></v-spacer>
            <v-card-actions>
                <v-dialog v-model="dialog" width="500">
                    <template v-slot:activator="{ on }">
                        <v-btn :disabled="file.isFolder"
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
                                    outline
                                    @click="dialog = false"
                            >
                                Отмена
                            </v-btn>

                            <v-btn
                                    color="secondary"
                                    outline
                                    v-clipboard:copy="secureLink.url"
                                    v-clipboard:success="clipboardSuccessHandler"
                                    v-clipboard:error="clipboardErrorHandler"
                                    @click="dialog = false"
                            >
                                Скопировать ссылку
                            </v-btn>

                            <v-btn
                                    color="success"
                                    outline
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
                <p>Полное имя файла: <u>"{{file.filename}}"</u></p>
                <span class="red--text"
                      v-if="file.isFolder">Чтобы создать ссылку на папку, поместите ее в архив</span>

                <div v-if="file.secureLinksCreated.length !== 0">
                    <h3>Созданные ранее ссылки</h3><br>
                    <table style="width: 100%">
                        <thead>
                        <tr>
                            <th class="text-xs-left">Кто создал</th>
                            <th class="text-xs-left">Время создания</th>
                            <th class="text-xs-left">Истекает</th>
                            <th class="text-xs-center">Ссылка</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="item in file.secureLinksCreated" :key="item.id">
                            <td>{{item.whoCreates.firstName}} {{item.whoCreates.lastName}}</td>
                            <td>{{humanDateTime(item.createTime)}}</td>
                            <td>{{humanDateTime(item.linkDeadline)}}</td>
                            <td>
                                                           <v-btn
                                    color="secondary"
                                    outline
                                    v-clipboard:copy="item.secureUrl"
                                    v-clipboard:success="clipboardSuccessHandler"
                                    v-clipboard:error="clipboardErrorHandler"
                                    @click="dialog = false"
                            >
                                Скопировать
                            </v-btn>
                            </td>
                        </tr>
                        </tbody>
                    </table>
                </div>

            </v-card-text>
        </v-slide-y-transition>
        <v-divider></v-divider>
    </v-card>
</template>

<script>
    import CREATE_SECURE_LINK from '../../../graphql/CreateSecureLink.gql'
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
            humanDateTime(val) {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(val);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")

            },
            dateModified(timestamp) {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(timestamp * 1000);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            },
            createLink(filename) {
                this.secureLink.url = '';
                this.secureLink.expires = 0;

                this.$apollo.mutate({
                    mutation: CREATE_SECURE_LINK,
                    variables: {
                        filename: filename
                    },
                }).then((data) => {
                    this.secureLink.url = data.data.createSecureLink.secureLink;
                    this.secureLink.expires = data.data.createSecureLink.linkDeadline;
                    this.dialog = true;
                }).catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }
                ));
            },
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