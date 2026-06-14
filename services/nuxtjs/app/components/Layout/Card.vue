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
        <div class="flex flex-col border border-gray-200 rounded-sm dark:border-gray-600 h-full">
            <div v-if="$slots.image" class="border-b border-gray-300 dark:border-gray-600">
                <slot name="image" />
            </div>            
            <div class="flex flex-row p-2 bg-gray-100 rounded-t-sm dark:bg-gray-700">
                <slot name="title" />
            </div>
            <div v-if="$slots.author" class="p-3 border-b border-gray-300 dark:border-gray-600">
                <slot name="author" />
            </div>
            <div class="p-3">
                <slot name="description" />
            </div>
            <div v-if="$slots.fields" class="p-3 border-t border-t-gray-300 dark:border-t-gray-600">
                <slot name="fields" />
            </div>
            <div v-if="$slots.button" class="p-3 border-t border-t-gray-300 dark:border-t-gray-600">
                <slot name="button" />
            </div>
            <div v-if="$slots.footer" class="border-t border-gray-200 dark:bg-gray-900 dark:border-t-gray-600 p-3 rounded-b-sm">
                <slot name="footer" />
            </div>
        </div>
    </div>
</template>