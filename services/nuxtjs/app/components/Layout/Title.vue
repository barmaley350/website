<script setup>
const props = defineProps({
    class: {
        type: [String, Array, Object],
        default: 'text-xl'
    }
})
</script>

<template>
    <div class="" :class="class">
        <slot />
    </div>
</template>