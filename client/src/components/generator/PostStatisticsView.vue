<template>
<div style="min-height:68vh">
    <q-card class="absolute-center  no-margin full-width full-height" square flat>
        <div class="row">
            <div class="col-5">
                <div class="text-h4 bg-grey-3 q-pa-sm">
                    Generated blocks
                </div>
                <q-scroll-area style="height:60vh">
                    <q-card square class="q-pa-md bg-grey-4" flat>
                        <div class="row justify-center">
                            <div v-for="(block, index) in $store.state.generated_blocks" :key="index">
                                <Block :block="block" :index="index" />
                            </div>
                        </div>
                    </q-card>
                </q-scroll-area>

            </div>
            <div class="col-7">
                <FailedStudents v-if="toggle" />
                <SuccessfulStudents v-if="!toggle" />
            </div>
        </div>
    </q-card>
    <div class="absolute-bottom-left q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
            <q-btn push class="bg-teal-3 text-white" size="md" label="toggle" @click="toggle=!toggle" />

        </q-btn-group>
    </div>

</div>
</template>

<script lang="js">
import {
    defineComponent,
} from 'vue';

import Block from '../statistics/Block.vue';
import FailedStudents from '../statistics/FailedStudents.vue';
import SuccessfulStudents from '../statistics/SuccessfulStudents.vue';

export default defineComponent({
    name: 'PostStatisticsView',
    emits: ["back", "next"],
    components: {
        // Subject,
        Block,
        // Student,
        SuccessfulStudents,
        FailedStudents
    },
    data() {
        return {
            toggle: false
        }
    },

});
</script>
