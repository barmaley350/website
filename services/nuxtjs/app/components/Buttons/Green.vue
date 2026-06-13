<script setup>
const props = defineProps({
    class: {
        type: [String, Array, Object],
        default: ''
    }
})
</script>

<template>
    <button class="bg-green-600 px-5 py-2 text-gray-100 rounded-sm" :class="class">
        <slot />
    </button>
</template>