<template>
    <div>
        <h1 class="mb-2">Добро пожаловать!</h1>
        <h3 class="mb-4">Приложение служит для быстрого создания публичных ссылок на&nbsp;файлы</h3>
        <v-divider></v-divider>
        <h4 class="mb-4">Как использовать:</h4>
        <ul>
            <li>
                <p>Чтобы создать ссылку, нужно зайти
                    <router-link to="/" target="_blank">сюда</router-link>
                    и&nbsp;нажать на&nbsp;кнопку &laquo;создать ссылку&raquo; напротив имени файла
                </p>
            </li>
            <li>
                <p>
                    Чтобы скопировать ссылку в&nbsp;буфер обмена, нужно нажать &laquo;скопировать ссылку&raquo;
                    в диалоговом окне, которое возникнет после нажатия кнопки "создать ссылку"
                </p>
            </li>
            <li>
                <p>
                    Ссылка существует 5&nbsp;дней по умолчанию (может быть изменено в настройках приложения). После
                    изменения времени жизни ссылки нужно будет создать новую ссылку, если это необходимо.
                </p>
            </li>
            <li>
                <p>
                    Чтобы досрочно удалить ссылку, нужно удалить, переместить или переименовать файл на&nbsp;файловой
                    системе.
                </p>
            </li>
            <li>
                <p class="body-2">
                    Если по&nbsp;какой-то причине файл пропадет с&nbsp;файловой системы, то&nbsp;и&nbsp;ссылка тоже
                    перестанет работать, так как это прямой доступ к&nbsp;файлу. Файл не&nbsp;копируется в&nbsp;облако,
                    и&nbsp;не&nbsp;кодируется, и&nbsp;вообще никаких манипуляций над файлами не&nbsp;производится.
                    Таким образом ссылка создается мнгновенно.
                </p>
            </li>
            <li>
                <p>
                    Сервис протестирован в&nbsp;браузерах: Google Chrome, Mozilla Firefox. Прочие браузеры могут
                    давать неожиданные результаты, просьба по&nbsp;возможности не&nbsp;пользоваться плохими и&nbsp;старыми
                    браузерами. (Включая IE и Edge всех версий)
                </p>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        name: "About"
    }
</script>

<style scoped>

</style>