<template>
    <v-flex xs12 sm6 offset-sm3>
        <v-card>
            <v-list two-line subheader>
                <v-subheader inset>Файлы</v-subheader>
                <template v-for="(item, index) in files">
                    <v-list-tile
                            :key="item.filename"
                            avatar
                            @click=""
                    >
                        <v-list-tile-avatar>
                            <v-icon class="grey lighten-1 white--text">{{ item.fileType }}</v-icon>
                        </v-list-tile-avatar>

                        <v-list-tile-content>
                            <v-list-tile-title>{{ item.filename }}</v-list-tile-title>
                            <v-list-tile-sub-title class="text--primary">{{ item.size }}</v-list-tile-sub-title>
                            <v-list-tile-sub-title>{{ item.modified }}</v-list-tile-sub-title>
                        </v-list-tile-content>
                        <v-list-tile-action>
                            <v-list-tile-action-text>bla</v-list-tile-action-text>
                        </v-list-tile-action>
                    </v-list-tile>
                    <v-divider
                            v-if="index + 1 < files.length"
                            :key="index"
                    ></v-divider>
                </template>
            </v-list>
        </v-card>
    </v-flex>
</template>

<script>
    import gql from 'graphql-tag'
    import FileListMenu from "./FileListMenu";

    const FILES = gql`query {
  files {
    size
    filename
    modified
    extension
    url
    fileType
  }
}
`;

    export default {
        name: "FileList",
        components: {FileListMenu},

        data() {
            return {
                files: [],
                valueDeterminate: 40
            }
        },
        apollo: {
            files: FILES,
        },
    }
</script>

<style scoped>

</style>