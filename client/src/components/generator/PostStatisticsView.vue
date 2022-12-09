<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-4">
                <q-card>
                    <q-card-section>
                        <div class="text-h6">Generated option blocks</div>
                    </q-card-section>
                    <q-scroll-area style="height: 100vh; max-width: 80vh;">
                        <div class="row justify-center">
                            <div v-for="(block, index) in $store.state.generated_blocks" :key="index">
                                <Block :block="block" :index="index" />
                            </div>
                        </div>
                    </q-scroll-area>
                </q-card>
            </div>
            <div class="col-8">
                    <q-card>
                        <q-card-section>
                            <div class="text-h6">Generated option blocks</div>
                            <!-- {{JSON.stringify($store.state.successful_students)}} -->
                            {{ $store.state.successful_students.length}}
                        </q-card-section>
                        <q-card-section>
                            <q-scroll-area style="height: 60vh;" class="q-mb-xl">

                                <div class="row justify-center">
                                    <div v-for="(student, index) in $store.state.successful_students" :key="index">
                                        <Student :student="student" :index="index" />
                                    </div>
                                </div>

                            </q-scroll-area>
                        </q-card-section>
                    </q-card>
            </div>
        </div>
    </q-card>
    <div class="absolute-bottom q-pa-sm">
        <!-- <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group> -->
    </div>
    <!-- <div class="absolute-bottom q-pa-md">
        </div>

        <div class="absolute-bottom-right q-pa-sm">
        </div> -->
</div>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';
import Block from '../statistics/Block.vue';
import Student from '../statistics/Student.vue';

export default defineComponent({
    name: 'PostStatisticsView',
    emits: ["back", "next"],
    components: {
        // Subject,
        Block,
        Student
    }

});
</script>
