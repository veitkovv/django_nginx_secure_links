<template>
    <v-container>
        <v-layout row wrap>
            <v-flex>
                <v-text-field
                        label="Проверка ссылки"
                        placeholder="Вставьте URL чтобы проверить срок ее жизни"
                        v-model="url"
                        @input="urlExpires()"
                        outline
                ></v-text-field>
                <h2 v-if="url">Ссылка истекает: {{linkDeadlineReadable}}</h2>
            </v-flex>
        </v-layout>
    </v-container>
</template>

<script>
    import CHECK_LINK_QUERY from '../../graphql/LinkDeadline.gql'

    export default {
        name: "CheckURL",
        data: () => ({
            url: '',
            linkDeadline: ''
        }),
        methods: {
            urlExpires() {
                this.$apollo.query({
                    query: CHECK_LINK_QUERY,
                    variables: {
                        url: this.url
                    }
                }).then(data => {
                    this.linkDeadline = data.data.linkDeadline
                })
            }
        },

        computed: {
            linkDeadlineReadable: function () {
                const moment = require('moment-timezone');
                const timezone = moment.tz.guess();
                let date = moment(this.linkDeadline);
                return date.tz(timezone).locale("ru").format("DD MMM YYYY H:mm")
            }
        }
    }
</script>

<style scoped>

</style>