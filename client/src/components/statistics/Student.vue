<template>
<q-card class="bg-grey-3" style="width:110vh;height:5.5vh" square flat>
    <div class="row justify-center">
        <q-separator />
        <div class="col-2 bg-grey-4">
            <q-btn color="grey" :label="student.uuid.slice(0,12)" size="sm" style="height: 5.5vh; width:15vh" square>
                <q-popup-proxy>
                    <q-banner>
                        <template v-slot:avatar>
                            <q-icon name="account_circle" color="light-grey" />
                        </template>
                        <div class="row">
                            student uuid: {{student.uuid}}
                        </div>
                        <div class="row">
                            student email: {{student.email }}
                        </div>
                    </q-banner>
                </q-popup-proxy>
            </q-btn>
        </div>

        <div class="col-4 q-pa-sm" style="height: 5vh;">
            {{student.name}}
        </div>
        <div class="col-3 q-pa-sm" style="height: 5vh;">
            {{student.pathway}}
        </div>

        <div class="col-3" >
            <div class="row float-right">
                <div v-for="(option) in student.options" :key="option">
                    <div :class="getOptionStyle(option[1]-1)" style="width:6vh;height:5.5vh">
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
        getOptionStyle(index) {
            let base = "q-pa-sm "
            base = base.concat(this.colours[index])
            return base
        }
    }
});
</script>
