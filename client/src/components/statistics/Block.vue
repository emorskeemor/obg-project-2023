<template>
<q-card :class="colours[index]" style="width:80vh">

    <div class="row">
        <div class="col bg-grey-3">
            <div class="text-h6 text-black q-pa-sm">Option Block [{{index+1}}]</div>
        </div>
        <div class="col-10">
            <div class="row">
                <div v-for="code in block" :key="code" style="padding:5px">
                    <Subject :code="code" />
                </div>
            </div>
        </div>
    </div>
</q-card>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';
import Subject from './Subject.vue';

export default defineComponent({
    name: 'OptionItem',
    props: ["block", "index"],
    components: {
        Subject
    },
    data() {
        return {
            colours: ["bg-red", "bg-orange", "bg-yellow", "bg-green"]
        }
    }

});
</script>
