<template>
    <div>
        <v-alert v-for="item in ALERTS"
                 :value="true"
                 :type="item.severity"
                 dismissible
                 transition="fade-transition"
        >
            {{item.text}}
        </v-alert>

    </div>
</template>

<script>
    import {mapGetters} from 'vuex';

    export default {
        name: "Alerts",
        computed: {
            ...mapGetters(['ALERTS'])
        }
    }
</script>

<style scoped>

</style>