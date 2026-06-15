<script setup>

const { statData, pending: pendingStat, error: errorStat } = useStatData()
const runtimeConfig = useRuntimeConfig()
const route = useRoute();
const id = route.params.id;

// let url = "baseURL" in runtimeConfig ? runtimeConfig.baseURL + 'objects/' + id : window.location.origin + '/backend/api/v1/objects/' + id
const apiUrl = process.server
    ? runtimeConfig.apiInternal      // на сервере — полный внутренний URL
    : runtimeConfig.public.apiBase   // на клиенте — относительный путь

const { data, status, error, pending } = await useFetch(`${apiUrl}objects/${id}`, {
    key: `objects-list-${id}`
})

const breadcrumbsData = computed(() => {
    // Здесь data.value уже точно существует (благодаря v-if)
    return [
        { url: `/objects/?category_id=${data.value.object.category_id}`, label: data.value.category.title, separator: true },
        { url: `/objects/${id}`, label: data.value.transaction.title, separator: true }
    ]
})

function getRandomFlatNumber() {
    return Math.floor(Math.random() * 53) + 1
}

</script>

<template>
    <div class="flex flex-col gap-3">
        <LayoutBreadcrumbs v-if="data" :breadcrumbsData></LayoutBreadcrumbs>
    </div>
    <div class="grid grid-cols-12 gap-3 mt-5">
        <div class="col-span-8">
            <div class="flex flex-col gap-3" v-if="data">
                <LayoutCardHorizontal>
                    <template #title>
                        <LayoutTitle class="text-xl font-bold">
                            {{ data.object.title }}
                        </LayoutTitle>
                        <!-- <LayoutBadges class="bg-green-200 text-gray-600" v-if="data.comments_count">
                            <Icon name="i-lucide:message-circle" /> {{ data.comments_count }}
                        </LayoutBadges>
                        <ButtonsGreen class="bg-green-600 ">
                            <Icon name="i-lucide:dollar-sign" /> {{ data.object.price.toLocaleString('ru-RU') }}
                        </ButtonsGreen> -->
                    </template>

                    <template #description>
                        <div class="flex flex-col gap-5">

                            <div class="">
                                <div class="flex justify-start">
                                    <div class="w-full">
                                        <img class=" h-full w-full object-cover rounded-lg"
                                            :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`">
                                    </div>
                                </div>
                            </div>
                            <div class="">

                                <div>{{ data.object.description }}</div>

                            </div>
                        </div>
                    </template>

                </LayoutCardHorizontal>
            </div>

        </div>
        <div class="col-span-4">
            <LayoutSidebarRight>
                <LayoutCardHorizontal>
                    <template #title>
                        <ButtonsGreen class="bg-green-600 ">
                            <Icon name="i-lucide:dollar-sign" /> {{ data.object.price.toLocaleString('ru-RU') }}
                        </ButtonsGreen>
                    </template>
                    <template #description>

                        <div class="flex flex-row justify-between py-1">
                            <div>Город</div>
                            <div>{{ data.city.title }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Тип сделки</div>
                            <div>{{ data.transaction.title }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Тип недвижимости</div>
                            <div class="text-right w-50">{{ data.category.title }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>E-Mail</div>
                            <div>{{ data.user.email }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Телефон</div>
                            <div>{{ data.user.phone }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Дата размещения</div>
                            <div>{{ data.object.created_at?.replace('T', ' ').split('.')[0] || '' }}</div>
                        </div>
                    </template>
                </LayoutCardHorizontal>

            </LayoutSidebarRight>
        </div>
    </div>


    <div class="flex justify-center gap-5 p-10">
        <LayoutText>
            <template #header_primary>
                <LayoutTitle class="text-xl font-bold underline">
                    Похожие объекты
                </LayoutTitle>
            </template>
            <template #header_secondary>
                <LayoutTitle class="text-base">
                    Похожие объекты подбираются по категории, городу и типу сделки
                </LayoutTitle>
            </template>
        </LayoutText>
    </div>

    <div class="grid grid-cols-3 gap-5 mt-5">
        <!-- {{ data.similar_objects }} -->
        <LayoutCard v-for="similar_object in data.similar_objects" :key="similar_object.id">
            <template #image>
                <div class="w-full">
                    <img class=" h-64 w-full object-cover rounded-t-lg"
                        :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`">
                </div>
            </template>
            <template #title>
                <LayoutTitle class="text-2xl">{{ similar_object.title.slice(0, 50) }}</LayoutTitle>
                <!-- <TitlesRegularNormal></TitlesRegularNormal> -->
            </template>
            <template #description>
                {{ similar_object.description.slice(0, 300) }}
            </template>
        </LayoutCard>
    </div>
</template>