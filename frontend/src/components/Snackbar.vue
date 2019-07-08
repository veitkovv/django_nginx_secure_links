<template>
    <div>
        <v-snackbar
                auto-height
                right
                top
                v-model="SNACKBAR.visible"
                :timeout="SNACKBAR.timeout"
                :color="SNACKBAR.color"
                :multi-line="SNACKBAR.multiline"
        >
            {{ SNACKBAR.text }}

            <v-btn flat @click.native="closeSnackbar">Закрыть</v-btn>
        </v-snackbar>
    </div>
</template>

<script>
    import {mapMutations, mapGetters} from 'vuex'

    export default {
        data() {
            return {}
        },
        methods: {
            ...mapMutations(['closeSnackbar'])
        },
        computed: {
            ...mapGetters(['SNACKBAR'])
        }
    }
</script>