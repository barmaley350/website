<template>
    <span :title="fullDate">{{ humanDate }}</span>
</template>

<script setup>
import { formatDistanceToNow } from 'date-fns'
import { ru } from 'date-fns/locale'

const props = defineProps({
    date: [String, Date],
})

const fullDate = typeof props.date === 'string'
    ? new Date(props.date).toISOString()
    : props.date.toISOString()

const humanDate = formatDistanceToNow(props.date, {
    locale: ru,
    addSuffix: true,
})
</script>


<!-- <HumanDate :date="item.createdAt" /> -->
<!-- покажет: «2 дня назад», «месяц назад», «год назад» и т.п. -->
