<script setup>
// import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute()

const items = computed(() => [
    {
        label: 'Проекты',
        to: '/projects',
        active: route.path.startsWith('/projects')
    },
    // {
    //     label: 'Основатели',
    //     to: '/docs/components',
    //     active: route.path.startsWith('/docs/components')
    // },
    {
        label: 'Комментарии',
        to: 'https://go.nuxt.com/figma-ui',
        //target: '_blank'
    },
    {
        label: 'Разработчики',
        to: 'https://github.com/nuxt/ui/releases',
        //target: '_blank'
    },
    {
        label: 'Лента коммитов',
        to: 'https://github.com/nuxt/ui/releases',
        //target: '_blank'
    },
    {
        label: 'Объявления',
        to: 'https://github.com/nuxt/ui/releases',
        //target: '_blank'
    },
])
</script>

<template>
    <UHeader :toggle="{
        color: 'primary',
        variant: 'subtle',
        class: 'rounded-full'
    }">
        <template #title>
            <LayoutLogo class="h-6 w-auto" />
        </template>

        <UNavigationMenu :items="items" />


        <template #right>

            <UButton color="neutral" variant="ghost" to="https://github.com/nuxt/ui" target="_blank"
                icon="i-material-symbols:login" aria-label="Регистрация">Вход</UButton>
            <UButton color="neutral" variant="ghost" to="https://github.com/nuxt/ui" target="_blank"
                icon="i-material-symbols-how-to-reg" aria-label="Регистрация">Регистрация</UButton>

            <UColorModeButton />
            <UTooltip text="Open on GitHub" :kbds="['meta', 'G']">
                <UButton color="neutral" variant="ghost" to="https://github.com/barmaley350/website" target="_blank"
                    icon="i-simple-icons-github" aria-label="GitHub" />
            </UTooltip>

        </template>

        <template #body>
            <UNavigationMenu :items="items" orientation="vertical" class="-mx-2.5" />
        </template>
    </UHeader>
</template>
