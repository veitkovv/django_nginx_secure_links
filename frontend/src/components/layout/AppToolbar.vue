<template>
    <v-toolbar scroll-toolbar-off-screen color="primary" dark fixed prominent app>
        <v-toolbar-side-icon @click.stop="changeNavDrawerState"></v-toolbar-side-icon>
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
    export default {
        name: "AppToolbar",
        methods: {
            changeNavDrawerState() {
                this.$store.dispatch('changeSidenavDrawerState').then(() => {
                    console.log('nav state changed')
                })
            },
            refetchFiles() {
                this.$store.dispatch('getFiles').then(() => console.log('Список файлов получен с сервера'))
            },
            doLogout() {
                this.$store.dispatch('logout').then(() => this.$store.dispatch('showAlert', {
                    text: 'Вы успешно вышли из системы',
                })).then(() => this.$router.push('/login'))
            }
        }
    }
</script>
