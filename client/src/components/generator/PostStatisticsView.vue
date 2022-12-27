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
                        <div v-if="failed" style="height:60vh">
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
    <q-dialog v-model="failed" persistent>
        <q-card>
            <q-card-section>
                <div class="text-h6 text-center">There's some bad news...</div>

            </q-card-section>

            <q-card-section class="q-pt-none text-body1">
                We could not generate any blocks with these configurations and the data provided. This is most likely
                due to rules that were put in place causing the blocks that were generated to not pass requirements. It may
                also be due to the the protocol that is being used.
            </q-card-section>

            <q-card-actions align="right">
                <q-btn flat label="RESTART" color="primary" @click="restart" />
            </q-card-actions>
        </q-card>
    </q-dialog>
    <div class="absolute-bottom-left q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="pre statistics" icon="trending_up" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="live update" icon="update" @click="$emit('next')" />
            <q-btn push class="bg-teal-3 text-white" size="md" :label="toggle ? 'successful students' : 'unsuccessful students'" @click="toggle=!toggle" />

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
            toggle: false,
            failed: !this.$store.state.rules_followed
        }
    },
    methods: {
        restart() {
            this.$router.push({
                "name": "room-edit",
                params: {
                    user_id: this.$route.params.user_id,
                    room_id: this.$route.params.room_id,
                }
            })
        }
    }

});
</script>
