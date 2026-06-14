<script setup>
const props = defineProps(['breadcrumbsData'])

const localBreadcrumbsData = [
    {
        url: "/",
        label: "Главная",
        separator: false,
    },
    {
        url: "/objects",
        label: "Объекты",
        separator: true,
    },
]

let localData

if (props.breadcrumbsData && props.breadcrumbsData.length > 0) {
    // Если пропс существует и не пуст, добавляем его элементы в начало
    localData = [...localBreadcrumbsData, ...props.breadcrumbsData];
} else {
    // Иначе используем только локальный массив
    localData = [...localBreadcrumbsData];
}

</script>

<template>
    <div class="flex flex-row">
        <div class="flex flex-row" v-for="item in localData" :key="item.label">
            <div class="mx-3" v-if="item.separator">
                <Icon name="i-lucide:arrow-right" />
            </div>
            <NuxtLink class="navbar-brand hover:underline underline-offset-4" :to=item.url>{{ item.label }}</NuxtLink>
        </div>
    </div>
</template>