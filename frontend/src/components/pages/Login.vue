<template>
    <v-layout align-center justify-center>
        <v-flex xs12 sm8 md4>
            <v-card class="elevation-12" v-if="IS_AUTHENTICATED">
                <v-card-text>
                    Вы авторизованы
                    {{TOKEN_DATA}}
                    {{CURRENT_USER_DATA}}
                </v-card-text>
            </v-card>

            <v-card class="elevation-12" v-else>
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
                    <v-btn color="primary" @click="login">
                        Войти
                    </v-btn>
                </v-card-actions>
            </v-card>
        </v-flex>
    </v-layout>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "AppLogin",
        data: () => ({
            username: '',
            password: ''
        }),
        methods: {
            login() {
                this.$store.dispatch('login', {username: this.username, password: this.password}).then(() => {
                    console.log('success auth!');
                    this.$store.dispatch('verifyToken').then(() =>
                        this.$store.dispatch('showAlert', {
                            severity: 'success',
                            text: 'Успешная авторизация'
                        }).then(() => this.$store.dispatch('fetchUserData').then(() => this.$router.push('/')))
                    )
                }, error => {
                    this.$store.dispatch('showAlert', {
                        severity: 'error',
                        text: error.graphQLErrors,
                    }).then(() => console.log(error));
                })
            }
        },
        computed: {
            ...mapGetters(['IS_AUTHENTICATED', 'TOKEN_DATA', 'CURRENT_USER_DATA'])
        }
    }
</script>

<style scoped>

</style>