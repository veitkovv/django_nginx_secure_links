<template>
    <v-flex xs12 sm8 offset-sm2>
        <v-card>
            <v-list two-line subheader>
                <v-subheader inset>Файлы</v-subheader>
                <template v-for="(item, index) in FILES">
                    <v-list-tile
                            :key="item.id"
                            avatar
                            @click=""
                    >
                        <v-list-tile-avatar>
                            <v-icon class="grey white--text">{{ item.fileType }}</v-icon>
                        </v-list-tile-avatar>

                        <v-list-tile-content>
                            <v-list-tile-title>{{ item.filename }}</v-list-tile-title>
                            <v-list-tile-sub-title
                                    v-if="!item.isFolder"
                                    class="text--primary"
                            >
                                Изменено: {{dateModified(item.modified) }}
                            </v-list-tile-sub-title>
                            <v-list-tile-sub-title v-if="!item.isFolder">
                                Ссылка действительна до:
                            </v-list-tile-sub-title>
                        </v-list-tile-content>

                        <v-btn color="success" v-if="item.hasUrl">Скопировать ссылку</v-btn>
                        <v-btn color="primary" v-else>Создать ссылку</v-btn>
                        <file-list-menu :item="item"></file-list-menu>

                        <v-list-tile-action>
                            <v-list-tile-action-text>
                                {{humanFileSize(item.size, true)}}
                            </v-list-tile-action-text>
                        </v-list-tile-action>
                    </v-list-tile>
                    <v-divider
                            v-if="index + 1 < FILES.length"
                            :key="index"
                    ></v-divider>
                </template>
            </v-list>
        </v-card>
    </v-flex>
</template>

<script>
    import FileListMenu from "./FileListMenu";
    import {mapGetters} from 'vuex';


    export default {
        name: "FileList",
        components: {FileListMenu},
        props: ['search'],

        data() {
            return {
                valueDeterminate: 40,
            }
        },
        computed: {
            ...mapGetters(['FILES']),
        },
        methods: {
            getFiles() {
                this.$store.dispatch('getFiles')
            },
            dateModified(timestamp) {
                const moment = require('moment');
                let date = moment(timestamp * 1000);
                return date.locale("ru").format("DD MMM YYYY hh:mm")
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
        },
        mounted() {
            this.getFiles()
        }
    }
</script>

<style scoped>

</style>