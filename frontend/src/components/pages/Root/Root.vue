<template>
    <v-container fluid fill-heigh>
        <v-progress-linear v-if="$apollo.loading" :indeterminate="true"></v-progress-linear>
        {{$apollo.loading}}
        {{loading}}
        <v-flex xs12 sm8 offset-sm2>
            <v-text-field v-model="search"
                          append-icon="search"
                          label="Поиск"
                          single-line
                          hide-details
            ></v-text-field>
            <file-list :files="EXISTING_FILES"></file-list>
        </v-flex>
    </v-container>
</template>

<script>
    import {mapGetters, mapActions} from 'vuex';
    import FileList from './FileList';

    export default {
        name: "FileListRoot",
        components: {FileList},

        data() {
            return {
                valueDeterminate: 40,
                search: '',
                loading: 0,
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
