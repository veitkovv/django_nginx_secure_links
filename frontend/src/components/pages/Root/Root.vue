<template>
    <v-container fluid fill-heigh>
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
    import {mapGetters} from 'vuex';
    import FileList from './FileList';

    export default {
        name: "FileListRoot",
        components: {FileList},

        data() {
            return {
                valueDeterminate: 40,
                search: '',
            }
        },
        computed: {
            ...mapGetters(['EXISTING_FILES']),
        },
        methods: {
            getFiles() {
                this.$store.dispatch('getFiles')
            },

        },
        mounted() {
            this.getFiles()
        }
    }
</script>
