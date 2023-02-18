<template>
<q-page class="q-pa-none no-scroll" padding>
    <div class="q-pa-md" style="width:100%">
        <div class="row q-gutter-xl">
            <div class="col-8">
                <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font">Current Rules</div>
                    </q-card-section>
                    <q-card-section class="col">
                        <div class="text-body1 q-ma-sm">
                            Rules define subjects that must be inserted together. This can be useful when you do not want two
                            subjects to not be chosen together. A way to avoid this is to insert subjects at the same time into
                            the same block.
                        </div>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching" class="full-height">
                                <div class="row justify-center items-center bg-grey-4">
                                    <div class="col-1 q-pa-md">
                                        ID
                                    </div>
                                    <div class="col q-pa-sm">
                                        Target
                                    </div>
                                    <div class="col q-pa-sm">
                                        Targets
                                    </div>
                                    <div class="col q-pa-sm">
                                        Actions
                                    </div>
                                </div>
                                <q-scroll-area class="col" visible style="height:48vh">
                                    <q-card v-for="insert in inserts" :key="insert.pk" flat square>
                                        <div class="row justify-center items-center">
                                            <div class="col-1 q-pa-lg">
                                                {{ insert.pk }}
                                            </div>
                                            <div class="col">
                                                <q-btn color="grey" :label="insert.target.title" size="md" style="width:80%">
                                                    <q-popup-proxy>
                                                        <q-banner>
                                                            <template v-slot:avatar>
                                                                <q-icon name="subject" color="light-grey" />
                                                            </template>
                                                            <div class="row">
                                                                target uuid: {{insert.target.uuid}}
                                                            </div>
                                                            <div class="row">
                                                                target code: {{insert.target.subject_code }}
                                                            </div>
                                                        </q-banner>
                                                    </q-popup-proxy>
                                                </q-btn>
                                            </div>
                                            <div class="col">
                                                <q-btn color="grey" :label="insert.targets.length == 1 ? insert.targets[0].title :`${insert.targets[0].title}...` " size="md" style="width:80%">
                                                    <q-badge color="purple" floating>
                                                        {{ insert.targets.length }}
                                                    </q-badge>
                                                    <q-popup-proxy>

                                                        <q-banner>
                                                            <template v-slot:avatar>
                                                                <q-icon name="subject" color="light-grey" />
                                                            </template>
                                                            <div v-for="subject in insert.targets" :key="subject.uuid">
                                                                {{ subject.title }}
                                                            </div>
                                                        </q-banner>
                                                    </q-popup-proxy>
                                                </q-btn>
                                            </div>
                                            <div class="col">
                                                <q-btn label="delete" push color="red" @click="deleteInserts(insert.pk)"/>
                                            </div>
                                        </div>
                                    </q-card>
                                    <q-card v-if="inserts.length <= 0" style="min-height:10vh">
                                        <q-card-section>
                                            <div class="text-h5 main-font">No rules have been defined for this room</div>
                                        </q-card-section>
                                    </q-card>
                                </q-scroll-area>
                                
                               
                            </div>
                        </transition>

                    </q-card-section>
                    <q-card-section class="bg-grey-4 absolute-bottom">
 
                    </q-card-section>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <!-- generated blocks -->
            <div class="col">
                <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font">Create</div>
                    </q-card-section>
                    <q-card-section>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching" class="full-height">
                                <div class="row items-center justify-center q-gutter-md">
                                    <div class="main-font text-body1">
                                        Any time the <b>'primary target'</b> subject will be inserted into the block, we can also insert other
                                        <b>'targets'</b> subjects to be inserted at the same time. 
                                    </div>

                                    <div class="row full-width justify-center ">
                                        <q-select v-model="target" 
                                        style="width:40vh" 
                                        :options="availableOptions" 
                                        label="primary target" dense 
                                        hint="the target subject" map-options />

                                    </div>
                                    <div class="row full-width justify-center ">
                                        <q-select v-model="targets" 
                                        style="width:40vh" multiple 
                                        :options="availableOptions" 
                                        use-chips label="targets" dense 
                                        hint="select subjects that will be inserted with the target" map-options />
                                    </div>
                                    <div class="row full-width justify-center items-center">
                                        <div class="row">
                                            <q-toggle v-model="strict" label="Strict Insertion" checked-icon="check" unchecked-icon="clear" />
                                        </div>
                                        <div class="main-font text-body2 q-pa-sm">
                                           <b>'Strict Insertion'</b> will prevent students from being able to pick the primary target with the target subjects
                                            when the student enters their options. If this is <b>disabled</b> it will only affect the generation process and not directly
                                            enforce it when students are picking their options.
                                        </div>

                                    </div>
                                </div>
                            </div>
                        </transition>

                    </q-card-section>
                    <q-card-section class="bg-grey-4 absolute-bottom">
                        <q-btn label="Create" color="teal-4" @click="createInsert" size="md" icon="done" />
                    </q-card-section>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
        </div>
    </div>
</q-page>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    ref,
    defineComponent
} from 'vue';

import draggable from "vuedraggable";

export default defineComponent({
    name: 'RuleEditorView',
    beforeMount() {
        this.getInserts()
    },
    data() {
        return {
            inserts: [],
            fetching: true,
            availableOptions: [],
            targets: [],
            target: ref(null),
            strict: false,
        }
    },
    methods: {
        getInserts() {
            this.fetching = true

            axiosInstance.get(`api-generate/together/${this.$route.params.room_id}/room-rules/`).then(
                response => {
                    this.inserts = response.data.inserts
                    this.availableOptions = response.data.available_options
                    this.fetching = false

                }
            )
        },
        createInsert() {
            if (this.target !== null) {
                this.fetching = true
                axiosInstance.post(`api-generate/together/`, {
                    room_code: this.$route.params.room_id,
                    target_pk: this.target.value,
                    targets: this.targets
                }).then(
                    response => {
                        this.getInserts()
                    }
                )
            }

        },
        deleteInserts(pk){
            this.fetching = true
            axiosInstance.delete(`api-generate/together/${pk}`).then(
                response=>{
                    this.getInserts()
                }
            )
        },
    }

});
</script>
