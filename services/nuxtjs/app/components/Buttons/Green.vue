<script setup>
const props = defineProps({
    class: {
        type: [String, Array, Object],
        default: ''
    }
})
</script>

<template>
    <button class="px-5 py-2 text-gray-100 rounded-sm text-2xl font-bold text-nowrap ml-5" :class="class">
        <slot />
    </button>
</template>