<script setup>
const isOpen = ref(false)
</script>

<template>
    <div class="relative inline-block">
        <!-- Кнопка -->
        <button @click="isOpen = !isOpen" aria-haspopup="true" :aria-expanded="isOpen"
            class="flex items-center space-x-1 bg-blue-500 text-white px-2 py-1 rounded focus:outline-none focus:ring-2 focus:ring-blue-600">
            Меню
            <Icon name="i-lucide:arrow-down" v-if="isOpen" />
            <Icon name="i-lucide:arrow-up" v-else />
        </button>

        <!-- Меню -->
        <div v-show="isOpen" @click="isOpen = false"
            class="text-gray-700 absolute mt-2 w-62 bg-white border border-gray-400 rounded shadow-lg z-50 dark:bg-gray-700">
            <a href="/drf/api/v1/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API DRF</div>
                <!-- <Icon name="i-lucide:arrow-up-right" /> -->
            </a>
            <a href="/fastapi/api/v1/projects" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API FastAPI</div>
                <!-- <Icon name="i-lucide:arrow-up-right" /> -->
            </a>
            <div class="border-b border-gray-400"></div>
            <a href="/drf/admin/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>Django Admin</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/adminer/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>Adminer</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/jupyter/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>Jupyter</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <div class="border-b border-gray-400"></div>
            <a href="/drf/sphinx/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>DRF models docs</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/drf/swagger/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API DRF / Swagger</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/drf/redoc/" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API DRF / Redoc</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/fastapi/docs" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API FastAPI / Swagger</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
            <a href="/fastapi/redoc" target="_blank"
                class="flex justify-between items-center space-x-3 px-4 py-2 text-gray-900 dark:text-white hover:text-gray-900 hover:bg-gray-100">
                <div>API FastAPI / Redoc</div>
                <LayoutBadges class="bg-red-200 dark:text-gray-900 rounded-sm">auth</LayoutBadges>
            </a>
        </div>
    </div>
</template>
