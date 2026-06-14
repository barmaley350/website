<script setup>
// let url = "baseURL" in runtimeConfig ? runtimeConfig.baseURL + 'objects' : window.location.origin + '/backend/api/v1/objects'
// const { data, status, error, pending } = useFetch(url, {
//     query: {
//         object_id: paginationPageNumber,
//     },
// })
const runtimeConfig = useRuntimeConfig()
const route = useRoute();
const id = route.params.id;

let url = "baseURL" in runtimeConfig ? runtimeConfig.baseURL + 'objects/' + id : window.location.origin + '/backend/api/v1/objects/' + id
const { data, status, error, pending } = useFetch(url)

const breadcrumbsData = [
    {
        url: "/objects/" + id,
        label: "Page #" + id,
        separator: true,
    },
]

</script>

<template>
    <div class="flex flex-col gap-3">
        <LayoutBreadcrumbs :breadcrumbsData></LayoutBreadcrumbs>
    </div>
    {{ data }}
</template>