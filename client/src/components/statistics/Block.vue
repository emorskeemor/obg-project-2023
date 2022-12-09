<template>
    <div class="row q-ma-sm" style="width:12vh">
        <q-card :class="colours[index]">
            <q-card-section >
                <div class="text-h6">Block {{index+1}}</div>
            </q-card-section>
            <div v-for="code in block" :key="code">
                <Subject :code="code"/>
            </div>
        </q-card>
    </div>
</template>
<script lang="js">
import { defineComponent } from 'vue';
import Subject from './Subject.vue';



export default defineComponent({
    name: 'OptionItem',  
    props: ["block", "index"],
    components: {
        Subject
    },
    data(){
        return {
            colours : ["bg-red", "bg-orange", "bg-yellow", "bg-green"]
        }
    }

});

</script>