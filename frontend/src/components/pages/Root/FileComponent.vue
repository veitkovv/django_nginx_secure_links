<template>
    <v-list-tile avatar>
        <v-list-tile-avatar>
            <v-icon class="grey white--text">{{ file.fileType }}</v-icon>
        </v-list-tile-avatar>

        <v-list-tile-content>
            <v-list-tile-title>{{ file.filename }}</v-list-tile-title>
            <v-list-tile-sub-title class="text--primary">
                Файл изменен: {{dateModified(file.modified) }}
            </v-list-tile-sub-title>

            <v-list-tile-sub-title v-if="file.secureLink">
                <p v-if="file.secureLink.isExpired" style="color: red">
                    Ссылка действительна до {{linkDeadlineTime(file.secureLink.linkDeadline)}}</p>
                <p v-else>
                    Ссылка действительна до {{linkDeadlineTime(file.secureLink.linkDeadline)}}</p>
            </v-list-tile-sub-title>

        </v-list-tile-content>

        <div v-if="file.secureLink && !file.secureLink.isExpired">
            <v-btn
                    outline
                    color="success"
                    v-clipboard:copy="file.secureLink.url"
                    v-clipboard:success="clipboardSuccessHandler"
                    v-clipboard:error="clipboardErrorHandler">
                >
                Скопировать ссылку
            </v-btn>
        </div>

        <v-btn v-else
               outline
               color="primary"
               @click="createLink(file)"
        >Создать ссылку
        </v-btn>

        <v-menu bottom right>
            <template v-slot:activator="{ on }">
                <v-btn
                        flat
                        icon
                        color="primary"
                        v-on="on"
                >
                    <v-icon>more_vert</v-icon>
                </v-btn>
            </template>

            <v-list v-if="file.secureLink && !file.secureLink.isExpired">
                <v-list-tile @click="createLink(file)">
                    <v-icon>refresh</v-icon>
                    <v-list-tile-content>
                        Пересоздать ссылку
                    </v-list-tile-content>
                </v-list-tile>
            </v-list>
        </v-menu>

        <v-list-tile-action>
            <v-list-tile-action-text>
                {{humanFileSize(file.size, true)}}
            </v-list-tile-action-text>
        </v-list-tile-action>
    </v-list-tile>
</template>

<script>
    import CREATE_SECURE_LINK from '../../../graphql/CreateSecureLink.gql'
    import {mapActions, mapMutations} from 'vuex'

    export default {
        name: "FileComponent",
        props: {
            file: Object
        },
        data: () => ({}),
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
