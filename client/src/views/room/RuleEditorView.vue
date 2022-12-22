<template>
<q-page class="q-pa-xs no-scroll" padding>
    <div class="q-pa-md" style="width:100%">
        <div class="row q-gutter-xl">
            <div class="col-8">
                <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font">Current Rules</div>
                    </q-card-section>
                    <q-card-section class="col">
                        <div class="text-body2 q-ma-sm">
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

                                    </div>
                                </div>
                                <q-scroll-area class="col" visible style="height:50vh">
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
                                                <q-btn label="delete" push />
                                                <!-- <q-toggle v-model="" /> -->

                                            </div>
                                        </div>
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
                            <div v-show="!fetching">

                            </div>
                        </transition>

                    </q-card-section>
                    <q-card-section class="bg-grey-4 absolute-bottom">
                        <q-btn label="Save" color="teal-4" @click="saveSettings" size="md" icon="done" />
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
    defineComponent
} from 'vue';
import BannerComponent from '@/components/misc/BannerComponent.vue';
import AvailableOptionItem from '@/components/options/AvailableOptionItem.vue';
import OptionItem from '@/components/options/OptionItem.vue';
import SubjectInfoDialog from '@/components/options/SubjectInfoDialog.vue';

import draggable from "vuedraggable";

export default defineComponent({
    name: 'RuleEditorView',
    beforeMount() {
        this.getInserts()
    },
    data() {
        return {
            inserts: [],
            fetching: true
        }
    },
    methods: {
        getInserts() {
            this.fetching = true

            axiosInstance.get(`api-generate/together/${this.$route.params.room_id}/room-rules/`).then(
                response => {
                    this.inserts = response.data
                    this.fetching = false

                }
            )
        },
        createInsert() {
            console.log("creating");
        }
    }

});
</script>
