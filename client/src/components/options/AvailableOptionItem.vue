<template>
    <div class="row justify-center items-center">
        <q-card style="width:55vh;margin:1vh" class="bg-teal-3 glossy">
        <q-card-section @click="$emit('showInfo', element)">
            <div class="text-h5 text-white">{{element.title}}</div>
        </q-card-section>
        </q-card>
    </div>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'AvailableOption',  
    props: ["element"],
    emits: ["showInfo"]
});

</script>