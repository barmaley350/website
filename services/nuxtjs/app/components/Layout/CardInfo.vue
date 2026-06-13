<script setup>
const props = defineProps(['data'])
</script>

<template>
    <div class="flex justify-between">
        <div>Владелец</div>
        <div>{{ data.username }}</div>
    </div>
    <div class="flex justify-between">
        <div>E-Mail</div>
        <div>{{ data.email }}</div>
    </div>
    <div class="flex justify-between">
        <div>Телефон</div>
        <div>{{ data.phone }}</div>
    </div>
    <div class="flex justify-between">
        <div>Город</div>
        <div>{{ data.city }}</div>
    </div>
    <div class="flex justify-between">
        <div>Категория</div>
        <div>{{ data.category }}</div>
    </div>
    <div class="flex justify-between">
        <div>Тип предложения</div>
        <div>{{ data.transaction }}</div>
    </div>
    <div class="flex justify-between">
        <div>Дата создания</div>
        <div>{{ data.created_at }}</div>
    </div>
    <!-- <div class="flex justify-between">
        <div>Дата размещения</div>
        <div>{{ data.created_at }}</div>
    </div> -->
</template>