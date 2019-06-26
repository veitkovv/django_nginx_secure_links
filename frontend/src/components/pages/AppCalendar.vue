<template>
    <v-layout wrap>
        <v-flex
                xs12
                class="mb-3"
        >
            <v-sheet height="600">
                <v-calendar
                        ref="calendar"
                        v-model="start"
                        :type="type"
                        :end="end"
                        color="primary"
                        locale="ru-ru"
                        :weekdays="weekdays"
                ></v-calendar>
            </v-sheet>
        </v-flex>

        <v-flex
                sm4
                xs12
                class="text-sm-left text-xs-center"
        >
            <v-btn @click="$refs.calendar.prev()">
                <v-icon
                        dark
                        left
                >
                    keyboard_arrow_left
                </v-icon>
                Пред.
            </v-btn>
        </v-flex>
        <v-flex
                sm4
                xs12
                class="text-xs-center"
        >
            <v-select
                    v-model="type"
                    :items="typeOptions"
                    label="Type"
            ></v-select>
        </v-flex>
        <v-flex
                sm4
                xs12
                class="text-sm-right text-xs-center"
        >
            <v-btn @click="$refs.calendar.next()">
                След.
                <v-icon
                        right
                        dark
                >
                    keyboard_arrow_right
                </v-icon>
            </v-btn>
        </v-flex>
    </v-layout>
</template>

<script>
    export default {
        name: "AppCalendar",
        data: () => ({
            type: 'month',
            start: '2019-01-01',
            end: '2019-01-06',
            weekdays: [1, 2, 3, 4, 5, 6, 0],
            typeOptions: [
                {text: 'День', value: 'day'},
                {text: '4 дня', value: '4day'},
                {text: 'Неделя', value: 'week'},
                {text: 'Месяц', value: 'month'},
            ]
        })
    }
</script>

<style scoped>

</style>