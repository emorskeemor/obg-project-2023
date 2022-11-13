<template>
    <div class="row justify-center items-center">
        <q-card style="width:40vh;margin:1vh" class="bg-teal-3 glossy">
        <q-card-section>
            <q-skeleton type="text" />
        </q-card-section>
        <q-separator dark inset />
        <q-card-actions class="justify-center">
            <q-skeleton type="QBtn"/>
        </q-card-actions>
        </q-card>
    </div>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'SkeletonComponent',  
});

</script>