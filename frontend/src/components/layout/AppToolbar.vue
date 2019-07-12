<template>
    <v-toolbar scroll-off-screen color="primary" dark fixed prominent app>
        <v-toolbar-side-icon @click.stop="changeSidenavDrawerState"></v-toolbar-side-icon>
        <v-toolbar-title class="white--text">Secure Links</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
            <v-layout align-center>
                <span>Привет, {{FULLNAME()}}!</span>
            </v-layout>
            <v-btn icon @click="refetchFiles">
                <v-icon>refresh</v-icon>
            </v-btn>
            <v-btn icon @click="doLogout">
                <v-icon>exit_to_app</v-icon>
            </v-btn>
        </v-toolbar-items>
    </v-toolbar>
</template>

<script>
    import {mapMutations, mapActions, mapGetters} from 'vuex'

    export default {
        name: "AppToolbar",
        methods: {
            ...mapMutations(['showSnackbar']),
            ...mapActions(['changeSidenavDrawerState', 'fetchFileList', 'revokeToken']),
            ...mapGetters(['FULLNAME', 'WITHOUT_LINKS_ONLY']),

            refetchFiles() {
                this.fetchFileList({withoutLinksOnly: this.WITHOUT_LINKS_ONLY()})
                    .then(() => this.showSnackbar({
                        text: 'Список файлов получен с сервера'
                    }))
                    .catch(err => this.showSnackbar({
                        text: err,
                        color: 'error'
                    }))
            },
            doLogout() {
                this.revokeToken()
                    .then(() => this.showSnackbar({
                            text: 'Вы успешно вышли из системы'
                        }), this.$router.push('/login')
                    ).catch(err => this.showSnackbar({
                    text: err,
                    color: 'error'
                }));
            }
        },
    }
</script>
