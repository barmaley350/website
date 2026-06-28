<script setup>
// import type { NavigationMenuItem } from '@nuxt/ui'

const route = useRoute()

const items = computed(() => [
    {
        label: 'Объекты',
        to: '/objects',
        active: route.path.startsWith('/docs/getting-started')
    },
    {
        label: 'Components',
        to: '/docs/components',
        active: route.path.startsWith('/docs/components')
    },
    {
        label: 'Figma',
        to: 'https://go.nuxt.com/figma-ui',
        target: '_blank'
    },
    {
        label: 'Releases',
        to: 'https://github.com/nuxt/ui/releases',
        target: '_blank'
    }
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
                icon="i-lucide:log-in" aria-label="Регистрация">Вход</UButton>
            <UButton color="neutral" variant="ghost" to="https://github.com/nuxt/ui" target="_blank"
                aria-label="Регистрация">Регистрация</UButton>
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
