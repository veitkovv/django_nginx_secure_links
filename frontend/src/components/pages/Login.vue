<template>
    <v-layout align-center justify-center row fill-height>
        <v-flex xs12 sm7 md4>
            <v-card class="elevation-12" v-if="IS_AUTHENTICATED">
                <v-card-text>
                    Вы авторизованы!
                    <ul>
                        <li> {{TOKEN_DATA}}</li>
                        <li> {{CURRENT_USER_DATA}}</li>
                    </ul>
                </v-card-text>
            </v-card>

            <v-card class="elevation-12 mt-4" v-else>
                <v-toolbar dark color="primary">
                    <v-toolbar-title>Пожалуйста, авторизуйтесь</v-toolbar-title>
                    <v-spacer></v-spacer>
                </v-toolbar>
                <v-card-text>
                    <v-form>
                        <v-text-field prepend-icon="person" name="login" label="Логин"
                                      type="text" v-model="username"></v-text-field>
                        <v-text-field prepend-icon="lock" name="password" label="Пароль" id="password"
                                      type="password" v-model="password"></v-text-field>
                    </v-form>
                </v-card-text>
                <v-card-actions>
                    <v-spacer></v-spacer>
                    <v-btn color="primary" @click.native="appLogin">
                        Войти
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import {mapGetters, mapMutations, mapActions} from 'vuex';

    export default {
        name: "AppLogin",
        data: () => ({
            username: '',
            password: '',
        }),
        methods: {
            ...mapActions([
                'doLogin',
                'verifyToken',
                'fetchUserData',
                'fetchDefaultSettings'
            ]),
            ...mapMutations(['showSnackbar']),
            appLogin() {
                this.doLogin({
                    username: this.username,
                    password: this.password
                }).then(() => {
                    this.verifyToken()
                        .then(() => this.fetchUserData()
                            .then(() => {
                                this.fetchDefaultSettings();
                                this.showSnackbar({text: 'Успешная авторизация', color: 'success'});
                                this.$router.push('/')
                            }))
                }, error => {
                    this.showSnackbar({text: error, color: 'error'});
                })
            },
        },
        computed: {
            ...mapGetters([
                'IS_AUTHENTICATED',
                'TOKEN_AUTH',
                'TOKEN_DATA',
                'CURRENT_USER_DATA',
                'CSRF_TOKEN',
            ])
        },
    }
</script>

<style scoped>

</style>