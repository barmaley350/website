<script setup>
const props = defineProps(['breadcrumbsData'])
const { page } = usePaginationState()
const { filters, setFilter, resetFilters } = useFiltersState()

const localBreadcrumbsData = [
    {
        to: "/",
        label: "Главная",
        icon: 'i-lucide-book-open',
        separator: false,
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
    <div class="flex flex-row mt-5 align-center">
        <div class="flex flex-row items-center" v-for="item in localData" :key="item.label">
            <Icon class="mx-1" name="i-lucide:arrow-right" v-if="item.separator" />
            <Icon class="mr-1" :name="item.icon" v-if="item.icon" />
            <NuxtLink class="navbar-brand hover:underline underline-offset-4" :to=item.to v-if="item.to">
                {{ item.label }}
            </NuxtLink>
            <span v-else>{{ item.label }}</span>
        </div>
    </div>
</template>