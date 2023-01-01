<template>
<div v-for="block in blocks" :key="block.id">
    <div class="row justify-center items-center">
        <q-card style="width:55vh;margin:1vh" class="bg-teal-3 glossy">
            <q-card-section>
                <div class="text-h5 text-white">{{block.title}}/{{block.room.code}}</div>
            </q-card-section>
            <q-card-actions>
                <q-btn class="bg-blue-grey text-white" icon="highlight_off" @click="$emit('delete', block)" />
                <q-btn class="bg-blue text-white" icon="info" @click="$emit('info', block)" />

            </q-card-actions>
        </q-card>
    </div>
</div>
</template>

<script>
import { defineComponent } from 'vue';

export default defineComponent({
    name: "BlocksList",
    props: ["blocks"],
    emits: ["delete", "info"]
})
</script>
