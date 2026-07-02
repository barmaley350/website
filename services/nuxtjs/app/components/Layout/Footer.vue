<script setup lang="ts">
import type { FooterColumn } from '@nuxt/ui'

const columns: FooterColumn[] = [
    {
        label: 'Community',
        children: [
            {
                label: 'Nuxters',
                to: 'https://nuxters.nuxt.com',
                target: '_blank'
            },
            {
                label: 'Video Courses',
                to: 'https://masteringnuxt.com/nuxt3?ref=nuxt',
                target: '_blank'
            },
            {
                label: 'Nuxt on GitHub',
                to: 'https://github.com/nuxt',
                target: '_blank'
            }
        ]
    },
    {
        label: 'Solutions',
        children: [
            {
                label: 'Nuxt Content',
                to: 'https://content.nuxt.com/',
                target: '_blank'
            },
            {
                label: 'Nuxt DevTools',
                to: 'https://devtools.nuxt.com/',
                target: '_blank'
            },
            {
                label: 'Nuxt Image',
                to: 'https://image.nuxt.com/',
                target: '_blank'
            },
            {
                label: 'Nuxt UI',
                to: 'https://ui.nuxt.com/',
                target: '_blank'
            }
        ]
    }
]
</script>

<template>
    <UFooterColumns :columns="columns" class="my-10">
        <template #right>
            <UFormField name="email" label="Subscribe to our newsletter" size="lg">
                <UInput type="email" class="w-full">
                    <template #trailing>
                        <UButton type="submit" size="xs" color="neutral" label="Subscribe" />
                    </template>
                </UInput>
            </UFormField>
        </template>
    </UFooterColumns>
</template>


<!-- <script setup>
const currentYear = new Date().getFullYear()
</script>
<template>
    <div
        class="grid grid-cols-2 gap-5 bg-white dark:bg-gray-900 mt-20 border-t p-5 border-gray-200 dark:border-gray-600">
        <div class="text-left"></div>
        <div class="text-right">
            TestApp {{ currentYear }}
            <Icon name="i-lucide:copyright" />
        </div>
    </div>
</template> -->