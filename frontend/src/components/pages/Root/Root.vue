<template>
    <v-flex xs12 sm8 offset-sm2>
        <v-text-field v-model="search"
                      append-icon="search"
                      label="Поиск"
                      single-line
                      hide-details
        ></v-text-field>

        <v-list two-line subheader>
            <v-subheader inset>Файлы</v-subheader>
            <template v-for="(item, index) in EXISTING_FILES">
                <file-component :file="item" :key="item.id"></file-component>
                <v-divider
                        v-if="index + 1 < EXISTING_FILES.length"
                        :key="index"
                ></v-divider>
            </template>
        </v-list>

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
                // TODO https://github.com/apollographql/react-apollo/issues/1314
                // TODO loading always false bug
            }
        },
        computed: {
            ...mapGetters(['EXISTING_FILES']),
        },
        methods: {
            ...mapActions(['getFiles'])
        },
        mounted() {
            this.getFiles()
        }
    }
</script>
