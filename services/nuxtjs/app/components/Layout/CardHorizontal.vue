<script setup>
const props = defineProps({
    class: {
        type: [String, Array, Object],
        default: ''
    }
})
</script>

<template>
    <div class="flex flex-col gap-3" :class="class">
        <div class="flex flex-col border border-gray-200 rounded-sm dark:border-gray-600 h-full hover:shadow-sm">
            <div v-if="$slots.title"
                class="flex flex-row p-5 border-b border-b-gray-100  rounded-t-sm  dark:border-b-gray-600">
                <slot name="title" />
            </div>
            <div v-if="$slots.header" class=" p-3 border-b border-b-gray-100 dark:border-b-gray-600">
                <slot name="header" />
            </div>
            <div v-if="$slots.description" class=" p-3 border-b border-b-gray-100 dark:border-b-gray-600">
                <slot name="description" />
            </div>
            <div v-if="$slots.footer" class="p-3 rounded-b-sm">
                <slot name="footer" />
            </div>
        </div>
    </div>
</template>