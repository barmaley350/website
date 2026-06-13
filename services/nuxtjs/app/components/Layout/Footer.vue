<script setup>
const currentYear = new Date().getFullYear()
</script>
<template>
    <div
        class="grid grid-cols-2 gap-5 bg-white dark:bg-gray-900 mt-20 border-t p-5 border-gray-200 dark:border-gray-600">
        <div class="text-left"></div>
        <div class="text-right">
            TestApp {{ currentYear }}
            <Icon name="i-lucide:copyright" />
        </div>
    </div>
</template>