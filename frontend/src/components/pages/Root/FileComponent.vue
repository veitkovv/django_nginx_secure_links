<template>
    <v-card>
        <v-card-title primary-title>
            <v-list-tile-avatar color="grey darken-3">
                <v-icon class="grey white--text">{{ file.fileType }}</v-icon>
            </v-list-tile-avatar>
            <div>
                <div class="title">{{ file.filename }}</div>
                <span class="subheading">Изменено: {{dateModified(file.modified) }}</span><br>
                <div v-if="file.secureLink">
                    <span v-if="file.secureLink.isExpired" class="red--text">
                        Ссылка действительна до {{linkDeadlineTime(file.secureLink.linkDeadline)}}
                    </span>
                    <span v-else class="grey--text">
                                Ссылка действительна до {{linkDeadlineTime(file.secureLink.linkDeadline)}}
                    </span>
                </div>
            </div>
            <v-spacer></v-spacer>
            <v-card-actions>
                <!--Если файл-->
                <div v-if="!file.isFolder">
                    <v-btn v-if="file.secureLink && !file.secureLink.isExpired"
                           flat
                           color="primary"
                           v-clipboard:copy="file.secureLink.url"
                           v-clipboard:success="clipboardSuccessHandler"
                           v-clipboard:error="clipboardErrorHandler">
                        Скопировать ссылку
                    </v-btn>

                    <v-btn v-else
                           flat
                           @click="createLink(file)"
                    >Создать ссылку
                    </v-btn>
                </div>

                <!--Если папка-->
                <div v-else>
                    <v-btn v-if="file.secureLink && !file.secureLink.isExpired"
                           flat
                           color="success"
                           v-clipboard:copy="file.secureLink.url"
                           v-clipboard:success="clipboardSuccessHandler"
                           v-clipboard:error="clipboardErrorHandler">
                        Скопировать ссылку
                    </v-btn>

                    <v-tooltip v-else bottom>
                        <template v-slot:activator="{ on }">
                            <v-btn
                                    flat
                                    v-on="on"
                                    color="primary"
                                    @click="createFolderLink(file)"
                            >Создать ссылку на папку
                            </v-btn>
                        </template>
                        <span>Сервер создаст ссылку на архив без сжатия, это займет некоторое время</span>
                    </v-tooltip>
                </div>


                <v-btn icon @click.native="show = !show">
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
                <div v-if="file.isFolder">
                    <p>Папка содержит файлы: </p>
                    <v-btn v-if="file.secureLink && !file.secureLink.isExpired"
                           @click.native="createFolderLink(file)"
                           flat
                    >
                        Пересоздать ссылку на папку
                    </v-btn>
                </div>

                <div v-else>
                    <v-btn v-if="file.secureLink && !file.secureLink.isExpired"
                            @click="createLink(file)"
                            flat
                    >
                        Пересоздать ссылку
                    </v-btn>
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
        }),
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
            linkDeadlineTime(datetime) {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(datetime);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            },
            createLink(file) {
                this.$apollo.mutate({
                    mutation: CREATE_SECURE_LINK,
                    variables: {
                        fileId: file.id
                    },
                }).then(() => {
                    this.getFiles().then(() => {
                        this.showSnackbar({
                            text: 'Ссылка на файл "' + file.filename + '" успешно создана'
                        })
                    })
                });
            },
            createFolderLink(folder) {
                console.log(folder)
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
