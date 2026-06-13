<template>
    <div class="flex flex-col gap-20">
        <div class="
            flex flex-col gap-10
            border 
            border-gray-100
            bg-gray-200 
            rounded-sm 
            p-10 
            dark:bg-gray-900
            dark:border-gray-600">
            <div class="flex justify-center">
                <LayoutTitle class="text-9xl font-bold">Тестовый проект</LayoutTitle>
            </div>


            <div class="flex justify-center text-center mt-5">
                <LayoutTitle class="text-3xl text-gray-500 dark:text-gray-300">
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Quia, distinctio. Mollitia tempore ad et
                    ipsa qui id nobis explicabo laborum, ut, optio aperiam vel fuga voluptatibus quo. In, libero
                    accusamus.
                </LayoutTitle>
            </div>
            <div class="flex justify-center">
                <ButtonsGreen class="text-5xl">Тестовая кнопка</ButtonsGreen>
            </div>

        </div>

        <div class="flex justify-center">
            <LayoutText>
                <template #header_primary>
                    <LayoutTitle class="text-5xl font-bold underline">
                        Header Primary
                    </LayoutTitle>
                </template>
                <template #header_secondary>
                    <LayoutTitle class="text-2xl">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit. Laborum ea dignissimos eveniet expedita
                        in officiis quisquam, blanditiis ipsum pariatur tempore. Odio dicta esse cum totam. Facere
                        accusamus quae placeat labore?
                    </LayoutTitle>
                </template>
            </LayoutText>
        </div>

        <div class="flex justify-center gap-5">
            <LayoutCard v-for="index in 3" :key="index">
                <template #title>
                    <LayoutTitle class="text-2xl">Title {{ index }}</LayoutTitle>
                </template>
                <template #description>
                    Lorem ipsum dolor sit amet consectetur adipisicing elit. Quisquam itaque fuga ratione? Nostrum,
                    suscipit natus reiciendis, delectus officiis minima consequatur illum optio consectetur blanditiis
                    saepe eius culpa officia at. Id.
                </template>
            </LayoutCard>
        </div>



        <div class="flex justify-center">
            <LayoutText>
                <template #header_primary>
                    <LayoutTitle class="text-5xl font-bold underline">
                        Header Primary
                    </LayoutTitle>
                </template>
                <template #header_secondary>
                    <LayoutTitle class="text-2xl">
                        Lorem ipsum dolor sit amet consectetur adipisicing elit
                    </LayoutTitle>
                </template>
            </LayoutText>
        </div>

        <div class="grid grid-cols-3 gap-5">
            <LayoutCard v-for="index in 6" :key="index">
                <template #title>
                    <LayoutTitle class="text-2xl">Title {{ index }}</LayoutTitle>
                    <!-- <TitlesRegularNormal></TitlesRegularNormal> -->
                </template>
                <template #description>
                    Lorem ipsum dolor sit amet, consectetur adipisicing elit. Accusamus excepturi et nostrum. Eius non,
                    sit
                    excepturi dicta libero ratione voluptate facere quam cumque obcaecati exercitationem ullam rem
                    sapiente,
                    ad itaque.
                </template>
            </LayoutCard>
        </div>
    </div>

</template>