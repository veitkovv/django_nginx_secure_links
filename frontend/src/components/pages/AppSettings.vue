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
                        :min="MIN_TTL"
                        :max="MAX_TTL"
                        @end="sliderEnd()"
                        thumb-label
                ></v-slider>
            </v-flex>
            <hr>
        </div>
    </v-flex>
</template>

<script>
    import {mapGetters, mapMutations} from 'vuex';

    export default {
        name: "AppSettings",
        data: () => ({}),
        methods: {
            ...mapMutations(['SET_LINK_TTL']),
            sliderLabel(days) {
                return days + ' дней'
            },
            sliderEnd() {
                console.log('end')
            }
        },
        computed: {
            ...mapGetters(['CURRENT_USER_DATA', 'DEFAULT_SETTINGS', 'MIN_TTL', 'MAX_TTL', 'LINK_TTL']),
            isSuperUser: function () {
                return this.CURRENT_USER_DATA.isSuperuser
            },
            current: {
                get: function () {
                    return this.LINK_TTL
                },
                set: function (val) {
                    this.SET_LINK_TTL(val)
                }
            }
        },
        mounted() {
            // commit default value
            const ttl = Math.floor(this.CURRENT_USER_DATA.profile.urlTtl / (3600 * 24));
            this.SET_LINK_TTL(ttl)
        }
    }
</script>

