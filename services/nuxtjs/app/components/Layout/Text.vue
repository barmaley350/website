<script setup>
const props = defineProps({
    class: {
        type: [String, Array, Object],
        default: ''
    },
    class2: {
        type: [String, Array, Object],
        default: ''
    }
})
</script>
<template>
    <div class="flex flex-col gap-5">
        <div class="text-center" :class="class">
            <slot name="header_primary"></slot>
        </div>
        <div v-if="$slots.header_secondary" class="text-center" :class="class2">
            <slot name="header_secondary"></slot>
        </div>
    </div>
</template>