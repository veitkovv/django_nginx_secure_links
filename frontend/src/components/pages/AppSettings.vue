<template>
    <v-flex>
        <div class="pb-3" v-if="isSuperUser">
            <h1>Настройки администратора</h1>
        </div>
        <hr>
        <div class="mb-3 mt-3">
            <h1 class="mb-3 mt-3">Пользовательские настройки</h1>
            <hr>
            <h3 class="pt-3">Время жизни ссылки</h3>
            <v-flex xs12 sm6>
                <v-slider
                        v-model="current"
                        :label="sliderLabel(current)"
                        :min="MIN_URL_EXPIRES"
                        :max="MAX_URL_EXPIRES"
                        @change="sliderEnd(current)"
                        thumb-label
                        :loading="loading"
                        prepend-icon="access_time"
                ></v-slider>
            </v-flex>
            <hr>
        </div>
    </v-flex>
</template>

<script>
    import {mapGetters, mapMutations, mapActions} from 'vuex';

    export default {
        name: "AppSettings",
        data: () => ({
            loading: false,
        }),
        methods: {
            ...mapMutations(['SET_URL_EXPIRES', 'showSnackbar']),
            ...mapActions(['updateUrlExpires', 'fetchUserData']),
            sliderLabel(days) {
                return days + ' дней'
            },
            sliderEnd(val) {
                // update settings && refetch user data
                this.updateUrlExpires(val).then(() => {
                    this.showSnackbar({
                        text: 'Время жизни ссылки изменено. Не забудьте пересоздать ссылку на файл',
                        color: ''
                    })
                });
                this.fetchUserData();
            }
        },
        computed: {
            ...mapGetters([
                'CURRENT_USER_DATA',
                'MIN_URL_EXPIRES',
                'MAX_URL_EXPIRES',
                'URL_EXPIRES']),
            isSuperUser: function () {
                return this.CURRENT_USER_DATA.isSuperuser
            },
            current: {
                get: function () {
                    return this.URL_EXPIRES
                },
                set: function (val) {
                    this.SET_URL_EXPIRES(val)
                }
            }
        },
        mounted() {
            // commit default value
            const ttl = Math.floor(this.CURRENT_USER_DATA.profile.urlTtl / (3600 * 24));
            this.SET_URL_EXPIRES(ttl)
        }
    }
</script>

