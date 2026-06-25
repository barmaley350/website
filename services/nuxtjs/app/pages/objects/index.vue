<script setup>
const { statData, pending: pendingStat, error: errorStat } = useStatData()
const runtimeConfig = useRuntimeConfig()
const { page } = usePaginationState()
const { filters, setFilter, resetFilters } = useFiltersState()

const paginationPageNumber = page
// const paginationPageNumber = ref(1)
const route = useRoute();

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

const { data, status, error, pending } = await useFetch(`${apiUrl}objects/`, {
    query: queryParams,
    key: computed(() => `objects-list-${paginationPageNumber.value}-${category_id}`)
})

const countFlats = computed(() => {
    if (status.value == "success") {
        return data.value["count"]
    }
})

function getRandomFlatNumber() {
    return Math.floor(Math.random() * 53) + 1
}

const breadcrumbsData = computed(() => {
    // Здесь data.value уже точно существует (благодаря v-if)
    const items = []
    if (category_id.value !== undefined && data.value["category_name"]) {
        items.push({ url: `/objects/?category_id=${category_id.value}`, label: data.value["category_name"], separator: true })
    }
    return items
})

watch(paginationPageNumber, () => {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    // or instant: window.scrollTo(0, 0)
})

// if (filters.value.category_id !== category_id.value) {
//     setFilter('category_id', category_id.value)
//     paginationPageNumber.value = 1
// }
</script>
<template>
    <div class="flex flex-col gap-3">
        <LayoutBreadcrumbs :breadcrumbsData :key="JSON.stringify(breadcrumbsData)"></LayoutBreadcrumbs>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countFlats"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
        </div>

        <div class="grid grid-cols-12 gap-5">
            <div class="col-span-9">
                <div class="flex flex-col gap-10" v-if="data">
                    <LayoutCardHorizontal v-for="item in data.results">
                        <template #title>
                            <LayoutTitle class="text-xl grow font-bold">
                                <NuxtLink class="navbar-brand hover:underline underline-offset-4"
                                    :to="'/objects/' + item.object.id">{{ item.object.title }}</NuxtLink>

                            </LayoutTitle>
                            <LayoutBadges class="bg-gray-100 text-gray-600" v-if="item.comments_count">
                                <Icon name="i-lucide:message-circle" /> {{ item.comments_count }}
                            </LayoutBadges>
                            <ButtonsGreen class="bg-brand-600 ">
                                <Icon name="i-lucide:dollar-sign" /> {{ item.object.price.toLocaleString('ru-RU') }}
                            </ButtonsGreen>
                        </template>

                        <template #description>
                            <div class="grid grid-cols-3 gap-3">

                                <div class="">
                                    <div class="flex justify-start">
                                        <div class="w-64">
                                            <img class=" h-full w-full object-cover rounded-lg"
                                                :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`">
                                        </div>
                                    </div>
                                </div>
                                <div class="flex flex-col col-span-2 gap-5">
                                    <div class="flex flex-row justify-start text-xl gap-x-3">
                                        <div class="flex flex-row">

                                            <LayoutBadgesParams>
                                                {{ item.city.title }}
                                            </LayoutBadgesParams>
                                        </div>
                                        <div class="flex flex-row">

                                            <LayoutBadgesParams>
                                                {{ item.transaction.title }}
                                            </LayoutBadgesParams>
                                        </div>
                                        <div class="flex flex-row">

                                            <LayoutBadgesParams>
                                                {{ item.category.title }}
                                            </LayoutBadgesParams>
                                        </div>
                                    </div>
                                    <div>{{ item.object.description.slice(0, 300) }}</div>

                                </div>
                            </div>
                        </template>
                        <template #footer>
                            <div class="flex flex-row justify-end text-xl gap-x-3">
                                <div class="flex flex-row">

                                    <LayoutBadgesParams>
                                        {{ item.user.email }}
                                    </LayoutBadgesParams>
                                </div>
                                <div class="flex flex-row">

                                    <LayoutBadgesParams>
                                        {{ item.user.phone }}
                                    </LayoutBadgesParams>
                                </div>
                                <div class="flex flex-row">

                                    <LayoutBadgesParams>
                                        {{ item.object.created_at?.replace('T', ' ').split('.')[0] || '' }}
                                    </LayoutBadgesParams>
                                </div>
                            </div>

                        </template>
                    </LayoutCardHorizontal>
                </div>

            </div>
            <div class="col-span-3">
                <LayoutSidebarRight>
                    <LayoutCardHorizontal>
                        <template #description>
                            <div class="flex flex-row justify-between">
                                <div class="text-2xl">Всего объектов</div>
                                <div class="text-2xl font-bold">{{ countFlats.toLocaleString('ru-RU') }}</div>
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
                                <div class="flex flex-row justify-between py-1" v-for="item in statData.cities"
                                    :key="item.id">
                                    <div>{{ item.city }}</div>
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

                    <LayoutCardHorizontal>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По типам предложений</LayoutTitle>
                        </template>
                        <template #description>
                            <div v-if="pendingStat">Загрузка глобальных данных...</div>
                            <div v-else-if="errorStat">Ошибка загрузки глобальных данных</div>
                            <div v-else>
                                <div class="flex flex-row justify-between py-1" v-for="item in statData.transactions"
                                    :key="item.id">
                                    <div>{{ item.transaction }}</div>
                                    <div>{{ item.count }}</div>
                                </div>
                            </div>
                        </template>
                    </LayoutCardHorizontal>
                </LayoutSidebarRight>
            </div>
        </div>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countFlats"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
        </div>
    </div>
</template>