<template>
    <div class="row justify-center items-center">
        <q-card :style="itemStyle" class="bg-teal-3 glossy">
            <q-card-section style="padding:5px">
            <div class="text-h5 text-white">{{element.title}}</div>
            <slot/>
            </q-card-section>
            <q-card-actions>
                <q-btn class="bg-blue-grey text-white" @click="$emit('removeOption', element)" icon="highlight_off"/>
                <q-btn class="bg-blue text-white" @click="showInfo('showInfo', element)" icon="info"/>
            </q-card-actions>
        </q-card>
    </div>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'OptionItem',  
    props: ["element", "itemStyle" ,"index"],
    emits: ["showInfo", "removeOption"]
});

</script>