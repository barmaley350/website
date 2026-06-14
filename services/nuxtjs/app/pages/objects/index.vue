<script setup>
const { statData, pending: pendingStat, error: errorStat } = useStatData()
const runtimeConfig = useRuntimeConfig()
const paginationPageNumber = ref(1)
let url = "baseURL" in runtimeConfig ? runtimeConfig.baseURL + 'objects' : window.location.origin + '/backend/api/v1/objects'
const { data, status, error, pending } = useFetch(url, {
    query: {
        page: paginationPageNumber,
    },
})

const countFlats = computed(() => {
    if (status.value == "success") {
        return data.value["count"]
    }
})

function getRandomFlatNumber() {
    return Math.floor(Math.random() * 53) + 1
}

// const breadcrumbsData = [
//     {
//         url: "/test",
//         label: "Объекты1",
//         separator: true,
//     },
// ]

</script>
<template>

    <div class="flex flex-col gap-3">
        <LayoutBreadcrumbs></LayoutBreadcrumbs>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countFlats" />
        </div>

        <div class="grid grid-cols-12 gap-3">
            <div class="col-span-9">
                <div class="flex flex-col gap-3" v-if="data">
                    <LayoutCard v-for="item in data.results" :key="item.id">
                        <template #title>
                            <LayoutTitle class="text-xl grow font-bold">
                                <NuxtLink class="navbar-brand hover:underline underline-offset-4"
                                    :to="'/objects/' + item.id">{{ item.title }}</NuxtLink>

                            </LayoutTitle>
                            <ButtonsGreen class="text-2xl font-bold text-nowrap ml-5">
                                <Icon name="i-lucide:dollar-sign" /> {{ item.price }}
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
                                    <div>{{ item.description.slice(0, 300) }}</div>

                                    <div class="flex flex-row justify-end text-xl gap-x-3">
                                        <div class="flex flex-row">
                                            <Icon name="i-lucide:tags" />
                                            <LayoutBadges
                                                class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                                {{ item.city }}
                                            </LayoutBadges>
                                        </div>
                                        <div class="flex flex-row">
                                            <Icon name="i-lucide:tags" />
                                            <LayoutBadges
                                                class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                                {{ item.transaction }}
                                            </LayoutBadges>
                                        </div>
                                        <div class="flex flex-row">
                                            <Icon name="i-lucide:tags" />
                                            <LayoutBadges
                                                class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                                {{ item.category }}
                                            </LayoutBadges>
                                        </div>
                                    </div>


                                </div>
                            </div>
                        </template>
                        <template #footer>
                            <div class="flex flex-row justify-end text-xl gap-x-3">
                                <div class="flex flex-row">
                                    <Icon name="i-lucide:tags" />
                                    <LayoutBadges class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                        {{ item.city }}
                                    </LayoutBadges>
                                </div>
                                <div class="flex flex-row">
                                    <Icon name="i-lucide:tags" />
                                    <LayoutBadges class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                        {{ item.email }}
                                    </LayoutBadges>
                                </div>
                                <div class="flex flex-row">
                                    <Icon name="i-lucide:tags" />
                                    <LayoutBadges class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                        {{ item.phone }}
                                    </LayoutBadges>
                                </div>
                                <div class="flex flex-row">
                                    <Icon name="i-lucide:tags" />
                                    <LayoutBadges class="text-base ml-1 bg-gray-100 dark:bg-gray-700 rounded-sm">
                                        {{ item.created_at }}
                                    </LayoutBadges>
                                </div>
                            </div>

                        </template>
                    </LayoutCard>
                </div>

            </div>
            <div class="col-span-3">
                <LayoutSidebarRight>
                    <LayoutCard>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По городам</LayoutTitle>
                        </template>
                        <template #description>
                            <!-- {{ statData.cities }} -->
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
                    </LayoutCard>
                    <LayoutCard>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По категориям</LayoutTitle>
                        </template>
                        <template #description>
                            <!-- {{ statData.cities }} -->
                            <div v-if="pendingStat">Загрузка глобальных данных...</div>
                            <div v-else-if="errorStat">Ошибка загрузки глобальных данных</div>
                            <div v-else>
                                <div class="flex flex-row justify-between py-1" v-for="item in statData.categories"
                                    :key="item.id">
                                    <div>{{ item.category }}</div>
                                    <div>{{ item.count }}</div>
                                </div>
                            </div>
                        </template>
                    </LayoutCard>

                    <LayoutCard>
                        <template #title>
                            <LayoutTitle class="text-xl font-bold">По типам предложений</LayoutTitle>
                        </template>
                        <template #description>
                            <!-- {{ statData.cities }} -->
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
                    </LayoutCard>
                </LayoutSidebarRight>
            </div>
        </div>
        <div class="block my-3">
            <UPagination v-model:page="paginationPageNumber" :total="countFlats" />
        </div>
    </div>
</template>