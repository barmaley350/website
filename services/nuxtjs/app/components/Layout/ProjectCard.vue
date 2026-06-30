<script setup>
const props = defineProps(['class', 'data'])

function getRandomImage() {
    return Math.floor(Math.random() * 53) + 1
}
</script>

<template>
    <!-- {{ props.data }} -->
    <div class="flex flex-col gap-3 border border-gray-200 rounded-sm dark:border-gray-600 h-full hover:shadow-sm"
        :class="class" v-for="item in props.data.results" :key="JSON.stringify(item)">
        <!-- <div class="flex flex-col border border-gray-200 rounded-sm dark:border-gray-600 h-full hover:shadow-sm"> -->
        <div class="flex h-30 flex-row p-5 border-b border-b-gray-100 rounded-t-sm  dark:border-b-gray-600">
            <LayoutTitle class=" text-xl grow font-bold">
                <NuxtLink class="navbar-brand hover:underline underline-offset-4"
                    :to="'/projects/' + item.project.slug">{{ item.project.title.slice(0, 50) }}</NuxtLink>
            </LayoutTitle>
            <!-- <LayoutBadges class="" v-if="item.comments_count">
                <Icon name="i-lucide:message-circle" /> {{ item.comments_count }}
            </LayoutBadges> -->
        </div>
        <!-- <div class=" p-3 border-b border-b-gray-100 dark:border-b-gray-600">
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
                    <div class="font-bold text-gray-400">Команда</div>
                    <UAvatarGroup :max="3">
                        <UAvatar :src="`http://localhost:1338/img2/${getRandomImage()}.jpg`" :alt="user.name"
                            v-for="user in item.team_users" :key="user.id" />
                    </UAvatarGroup>
                </div>
            </div>
        </div> -->
        <div class=" p-3 border-b border-b-gray-100 dark:border-b-gray-600">
            <div>{{ item.project.description.slice(0, 300) }}</div>
        </div>
        <div class="p-3 rounded-b-sm">
            <div class="flex flex-row justify-between text-sm gap-x-3">
                <div class="flex flex-row items-center">
                    <div class="font-bold text-gray-400">Стек</div>
                    <LayoutBadgesParams v-for="skill in item.project_skills" :key="JSON.stringify(skill)"
                        class="flex flex-row items-center gap-1 text-sm p-1">
                        {{ skill }}
                    </LayoutBadgesParams>
                </div>

            </div>
        </div>
        <!-- </div> -->
    </div>
</template>