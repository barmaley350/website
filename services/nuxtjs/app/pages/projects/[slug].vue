<script setup>

const { statData, pending: pendingStat, error: errorStat } = useStatData()
const runtimeConfig = useRuntimeConfig()
const route = useRoute();
const slug = route.params.slug;

const apiUrl = process.server
    ? runtimeConfig.apiInternal      // на сервере — полный внутренний URL
    : runtimeConfig.public.apiBase   // на клиенте — относительный путь

const { data: dataObject, status: statusObject, error: errorObject, pending: pendingObject } = await useFetch(`${apiUrl}projects/${slug}`, {
    key: `project-${slug}`
})

const { data: dataRelatedObjects, status: statusRelatedObjects, error: errorRelatedObjects, pending: pendingRelatedObjects } = await useFetch(`${apiUrl}projects/${slug}/related/`, {
    key: `project-related-${slug}`
})

const breadcrumbsData = computed(() => {
    // Здесь data.value уже точно существует (благодаря v-if)
    return [
        {
            to: "/projects",
            label: "Проекты",
            separator: true,
            icon: 'i-lucide-box',
        },
        {
            // to: `/projects/?category_id=${dataObject.value.project.category_id}`,
            label: dataObject.value.project.title, separator: true, icon: "",
        },
    ]
})

function getRandomImage() {
    return Math.floor(Math.random() * 53) + 1
}

</script>

<template>
    <div class="flex flex-col gap-3">
        <LayoutBreadcrumbs v-if="dataObject" :breadcrumbsData></LayoutBreadcrumbs>
    </div>
    <div class="grid grid-cols-12 gap-3 mt-5">
        <div class="col-span-8">
            <div class="flex flex-col gap-3" v-if="dataObject">
                <LayoutCardHorizontal>
                    <template #title>
                        <LayoutTitle class="text-xl font-bold">
                            {{ dataObject.project.title }}
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

                            <!-- <div class="">
                                <div class="flex justify-start">
                                    <div class="w-full">
                                        <img class=" h-full w-full object-cover rounded-lg"
                                            :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`">
                                    </div>
                                </div>
                            </div> -->
                            <div class="">

                                <div>{{ dataObject.project.description }}</div>

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
                        <!-- <ButtonsGreen class="bg-brand-600 ">
                            <Icon name="i-lucide:dollar-sign" /> {{ dataObject.object.price.toLocaleString('ru-RU') }}
                        </ButtonsGreen> -->
                        <!-- {{ dataObject }} -->
                        <UAvatarGroup :max="3">
                            <UAvatar :src="`http://localhost:1338/img2/${getRandomImage()}.jpg`" :alt="user.name"
                                v-for="user in dataObject.team_users" :key="user.id" />
                        </UAvatarGroup>
                    </template>
                    <template #description>

                        <div class="flex flex-row justify-between py-1">
                            <div>Город</div>
                            <div>{{ dataObject.geo.name }}</div>
                        </div>
                        <!-- <div class="flex flex-row justify-between py-1">
                            <div>Тип сделки</div>
                            <div>{{ dataObject.transaction.title }}</div>
                        </div> -->
                        <div class="flex flex-row justify-between py-1">
                            <div>Тип недвижимости</div>
                            <div class="text-right w-50">{{ dataObject.category.name }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>E-Mail</div>
                            <div>{{ dataObject.user.email }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Телефон</div>
                            <div>{{ dataObject.user.phone }}</div>
                        </div>
                        <div class="flex flex-row justify-between py-1">
                            <div>Дата размещения</div>
                            <div>{{ dataObject.project.created_at?.replace('T', ' ').split('.')[0] || '' }}</div>
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
        <LayoutCard v-for="relatedObject in dataRelatedObjects.results" :key="relatedObject.project.id">
            <!-- <template #image>
                <div class="w-full">
                    <img class=" h-64 w-full object-cover rounded-t-lg"
                        :src="`http://localhost:1338/img2/${getRandomFlatNumber()}.jpg`">
                </div>
            </template> -->
            <template #title>
                <LayoutTitle class="text-2xl">
                    <NuxtLink class="navbar-brand hover:underline underline-offset-4"
                        :to="'/projects/' + relatedObject.project.slug">{{ relatedObject.project.title.slice(0, 50) }}
                    </NuxtLink>
                </LayoutTitle>
            </template>
            <template #description>
                {{ relatedObject.project.description.slice(0, 300) }}
            </template>
        </LayoutCard>
    </div>
</template>