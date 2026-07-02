<script setup>
const { statData, pending: pendingStat, error: errorStat } = useStatData()
const runtimeConfig = useRuntimeConfig()
const { page } = usePaginationState()
const { filters, setFilter, resetFilters } = useFiltersState()

const paginationPageNumber = page
// const paginationPageNumber = ref(1)
const route = useRoute();

const cardTypes = ref(['List', 'Card'])
const cardTypesValue = ref('List')

const category_id = computed(() => {
    const raw = route.query.category_id
    return raw ? Number(raw) : undefined
})

const apiUrl = process.server
    ? runtimeConfig.apiInternal      // на сервере — полный внутренний URL
    : runtimeConfig.public.apiBase   // на клиенте — относительный путь

const queryParams = computed(() => {
    const params = {}
    if (category_id.value !== undefined) {
        params.category_id = category_id.value
        // paginationPageNumber.value = 1
    }
    params.page = paginationPageNumber.value
    //TODO вынести в отдельную функцию
    if (filters.value.category_id !== category_id.value) {
        setFilter('category_id', category_id.value)
        paginationPageNumber.value = 1
    }
    return params
})

const { data, status, error, pending } = await useFetch(`${apiUrl}projects/`, {
    query: queryParams,
    key: computed(() => `projects-list-${paginationPageNumber.value}-${category_id}`)
})

const countProjects = computed(() => {
    if (status.value == "success") {
        return data.value["count"]
    }
})

const breadcrumbsData = computed(() => {
    // Здесь data.value уже точно существует (благодаря v-if)
    const items = [
        {
            // to: "/projects",
            label: "Проекты",
            separator: true,
            icon: 'i-lucide-box',
            count: countProjects.value,
        },
    ]
    if (category_id.value !== undefined && data.value["category_name"]) {
        items.push({ to: `/projects/?category_id=${category_id.value}`, label: data.value["category_name"], separator: true })
    }
    return items
})

watch(paginationPageNumber, () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    // or instant: window.scrollTo(0, 0)
})


</script>
<template>
    <div class="flex flex-col gap-3">
        <div class="flex flex-row justify-between items-center mt-5">
            <LayoutBreadcrumbs :breadcrumbsData :key="JSON.stringify(breadcrumbsData)"></LayoutBreadcrumbs>
            <div class="block">Всего проектов {{ countProjects.toLocaleString('ru-RU') }}</div>
        </div>

        <div class="flex flex-row justify-between items-center my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countProjects"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
            <div>
                <USelect v-model="cardTypesValue" :items="cardTypes" />
            </div>
        </div>
        <div class="grid grid-cols-12 gap-5">
            <div class="col-span-9">
                <div class="flex flex-col gap-10" v-if="data && cardTypesValue == 'List'">
                    <LayoutProjectList :data />
                </div>
                <div class="grid grid-cols-3 gap-4" v-else>
                    <LayoutProjectCard :data />
                </div>
            </div>
            <div class="col-span-3">
                <LayoutSidebarRight>
                    <LayoutCardHorizontal>
                        <template #description>
                            <div class="flex flex-row justify-between">
                                <div class="text-2xl">Всего объектов</div>
                                <div class="text-2xl font-bold">{{ countProjects.toLocaleString('ru-RU') }}</div>
                            </div>
                        </template>
                    </LayoutCardHorizontal>
                    <LayoutCardHorizontal>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По городам</LayoutTitle>
                        </template>
                        <template #description>
                            <div v-if="pendingStat">Загрузка глобальных данных...</div>
                            <div v-else-if="errorStat">Ошибка загрузки глобальных данных</div>
                            <div v-else>
                                <div class="flex flex-row justify-between py-1" v-for="item in statData.geos"
                                    :key="item.id">
                                    <div>{{ item.geo }}</div>
                                    <div>{{ item.count }}</div>
                                </div>
                            </div>
                        </template>
                    </LayoutCardHorizontal>
                    <LayoutCardHorizontal>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По категориям</LayoutTitle>
                        </template>
                        <template #description>
                            <div v-if="pendingStat">Загрузка глобальных данных...</div>
                            <div v-else-if="errorStat">{{ errorStat }}</div>
                            <div v-else>
                                <div class="flex flex-row justify-between py-1" v-for="item in statData.categories"
                                    :key="item.id">
                                    <div>{{ item.category }}</div>
                                    <div>{{ item.count }}</div>
                                </div>
                            </div>
                        </template>
                    </LayoutCardHorizontal>
                </LayoutSidebarRight>
            </div>
        </div>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countProjects"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
        </div>
    </div>
</template>