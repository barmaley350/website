<script setup>

const urls_left = {
    main: {
        url: "/",
        label: "LOGO",
        icon: "",
    },
    flats: {
        url: "/posts",
        label: "Посты",
        icon: "i-lucide-book-open",
    },
    // about: {
    //     url: "/about",
    //     label: "Информация",
    //     icon: "lucide:info",
    // },
}
const urls_right = {
    login: {
        url: "/login",
        label: "Вход",
        icon: "lucide:info",
    },
    registration: {
        url: "/login",
        label: "Регистрация",
        icon: "lucide:info",
    },
}
const colorMode = useColorMode()

const isDark = computed(() => colorMode.value === 'dark')

function toggleDarkMode() {
    colorMode.preference = isDark.value ? 'light' : 'dark'
}

</script>
<template>
    <div class="flex justify-between sticky top-0 z-50 py-5 px-5 bg-white dark:bg-gray-900">
        <div class="flex space-x-5 justify-start">
            <div class="flex items-center space-x-1 font-normal text-xl" v-for="url in urls_left">
                <NuxtLink class="navbar-brand" :to="url['url']">{{ url['label'] }}</NuxtLink>
            </div>
            <!-- <div class="flex items-center space-x-1 font-normal">
                <a href="/admin/" target="_blank">Django Admin</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div>

            <div class="flex items-center space-x-1 font-normal">
                <a href="/docs/index.html" target="_blank">Sphinx docs</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div>
            <div class="flex items-center space-x-1 font-normal">
                <a href="/adminer/" target="_blank">Adminer</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div>
            <div class="flex items-center space-x-1 font-normal">
                <a href="/api/" target="_blank">API DRF</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div>
            <div class="flex items-center space-x-1 font-normal">
                <a href="/fastapi/" target="_blank">API FastAPI</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div>
            <div class="flex items-center space-x-1 font-normal">
                <a href="/jupyter/" target="_blank">Jupyter</a>
                <Icon name="i-lucide:arrow-up-right" />
            </div> -->
        </div>
        <div class="flex items-center space-x-3 font-normal">
            <LayoutDropDownMenu></LayoutDropDownMenu>
            <div class="flex gap-x-2 px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md items-center">
                <Icon name="i-lucide:log-in" />
                <NuxtLink class="navbar-brand" :to="urls_right['login']['url']">Вход</NuxtLink>
            </div>

            <div class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md flex items-center">
                <NuxtLink class="navbar-brand" :to="urls_right['registration']['url']">Регистрация</NuxtLink>
            </div>

            <div class="h-full">
                <button @click="toggleDarkMode"
                    class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded-md flex items-center h-full">
                    <div class="flex" v-if="!isDark">
                        <Icon name="i-lucide:moon" />
                    </div>
                    <div class="flex" v-else>
                        <Icon name="i-lucide:sun" />
                    </div>
                </button>
            </div>

        </div>
    </div>
</template>