<template>
    <v-toolbar scroll-toolbar-off-screen color="primary" dark fixed prominent app>
        <v-toolbar-side-icon @click.stop="changeNavDrawerState"></v-toolbar-side-icon>
        <v-toolbar-title class="white--text">Secure Links</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-toolbar-items class="hidden-sm-and-down">
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
    import {mapMutations} from 'vuex'

    export default {
        name: "AppToolbar",
        methods: {
            ...mapMutations(['showSnackbar']),

            changeNavDrawerState() {
                this.$store.dispatch('changeSidenavDrawerState').then(() => {
                    console.log('nav state changed')
                })
            },
            refetchFiles() {
                this.$store.dispatch('getFiles').then(() =>
                    this.showSnackbar({
                        text: 'Список файлов получен с сервера'
                    })
                )
            },
            doLogout() {
                this.$store.dispatch('logout').then(() => this.$router.push('/login'));
                this.showSnackbar({
                    text: 'Вы успешно вышли из системы'

                })
            }
        }
    }
</script>
