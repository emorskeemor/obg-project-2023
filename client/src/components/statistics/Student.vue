<template>
<q-card class="bg-teal-3" style="width:100vh" square>
    <div class="row">
        <q-separator />
        <div class="col-1">
            {{index}}
        </div>

        <div class="col-5">
            {{student.id}}
        </div>
        <div class="col-3">
            {{student.pathway}}
        </div>

        <div class="col-3">
            <div class="row float-right">
                <div v-for="(option) in student.options" :key="option">
                    <div :class="getOptionStyle(option[1]-1)" style="width:6vh">

                        {{option[0]}}
                    </div>
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

export default defineComponent({
    name: 'OptionItem',
    props: ["student", "index"],
    data() {
        return {
            base: "bg-yellow",
            colours: ["bg-red", "bg-orange", "bg-yellow", "bg-green"]
        }
    },
    methods: {
        getOptionStyle(index){
            let base = "q-pa-sm "
            base = base.concat(this.colours[index])
            return base
        }
    }
});
</script>
