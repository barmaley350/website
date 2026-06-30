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

const { data, status, error, pending } = await useFetch(`${apiUrl}projects/`, {
    query: queryParams,
    key: computed(() => `projects-list-${paginationPageNumber.value}-${category_id}`)
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
    const items = [
        {
            to: "/projects",
            label: "Проекты",
            separator: true,
            icon: 'i-lucide-box',
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
        <LayoutBreadcrumbs :breadcrumbsData :key="JSON.stringify(breadcrumbsData)"></LayoutBreadcrumbs>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countFlats"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
        </div>
        <div class="grid grid-cols-12 gap-5">
            <div class="col-span-9">
                <div class="flex flex-col gap-10" v-if="data">
                    <LayoutCardHorizontal v-for="item in data.results" :key="JSON.stringify(item)">
                        <template #title>
                            <LayoutTitle class=" text-xl grow font-bold">
                                <NuxtLink class="navbar-brand hover:underline underline-offset-4"
                                    :to="'/projects/' + item.project.slug">{{ item.project.title }}</NuxtLink>
                            </LayoutTitle>
                            <LayoutBadges class="" v-if="item.comments_count">
                                <Icon name="i-lucide:message-circle" /> {{ item.comments_count }}
                            </LayoutBadges>
                        </template>
                        <template #header>
                            <div class="flex flex-row justify-between text-sm gap-x-3">
                                <div class="flex flex-row items-center gap-1">
                                    <div class="font-bold text-gray-400">Добавлен</div>
                                    <LayoutBadgesParams class="flex flex-row items-center gap-1 text-sm p-1">
                                        <LayoutHumanDate :date="item.project.created_at" />
                                    </LayoutBadgesParams>
                                    <div class="font-bold text-gray-400">Последня активность</div>
                                    <LayoutBadgesParams class="flex flex-row items-center gap-1 text-sm p-1">
                                        <LayoutHumanDate :date="item.project.created_at" />
                                    </LayoutBadgesParams>
                                </div>
                                <div class="flex flex-row items-center gap-1" v-if="item.team_users">
                                    <!-- <LayoutBadgesParams class="text-sm">Команда</LayoutBadgesParams> -->
                                    <div class="font-bold text-gray-400">Команда</div>
                                    <UAvatarGroup :max="3">
                                        <UAvatar :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`"
                                            :alt="user.name" v-for="user in item.team_users" :key="user.id" />
                                    </UAvatarGroup>
                                </div>
                            </div>
                        </template>
                        <template #description>
                            <div>{{ item.project.description.slice(0, 300) }}</div>
                        </template>
                        <template #footer>
                            <div class="flex flex-row justify-between text-sm gap-x-3">
                                <div class="flex flex-row items-center">
                                    <div class="font-bold text-gray-400">Стек</div>
                                    <LayoutBadgesParams v-for="skill in item.project_skills"
                                        :key="JSON.stringify(skill)"
                                        class="flex flex-row items-center gap-1 text-sm p-1">
                                        {{ skill }}
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
            <UPagination v-model:page="paginationPageNumber" :total="countFlats"
                :to="(page) => ({ query: { page, category_id: category_id } })" />
        </div>
    </div>
</template>