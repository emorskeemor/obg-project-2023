<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="q-pa-md">
            <q-card-section>
                <div class="row text-h4 items-center justify-center">
                    Ensure your settings are good to go
                    <div v-if="this.$store.state.using_database">
                        <q-chip icon="table">Using database</q-chip>
                    </div>
                    <div v-else>
                        <q-chip icon="folder">Using CSV</q-chip>
                    </div>

                </div>
            </q-card-section>
            <q-card-section>
                <div class="row q-gutter-xl">
                    <div class="col">

                        <q-card class="q-pa-md bg-white" style="min-height:50vh">
                            <div class="text-h4 text-center">Generation Settings</div>
                            <div class="text-body1 text-center">
                                The settings are READ ONLY and can be edited using the button at the bottom
                                of the page
                            </div>

                            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                                <div class="row q-gutter-md">
                                    <div class="col q-gutter-md">
                                        <q-input v-model="settingsTitle" autofocus outlined label="title" type="text" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="blocks" autofocus filled label="blocks" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="grid_view" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="currency_pound" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <div class="col q-gutter-md">
                                        <q-input v-model="classSize" autofocus filled label="class size" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="school" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>
                                        <q-toggle v-model="blocksMustAlign" disable label="blocks must algin" />

                                    </div>
                                </div>
                            </transition>
                            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />
                        </q-card>
                    </div>

                    <div class="col">
                        <q-card class="q-pa-md bg-white" style="min-height:50vh">
                            <div class="text-h4 text-center">Rules</div>
                            <div class="text-body1 text-center">
                                The rules are READ ONLY and can be edited using the button at the bottom
                                of the page
                            </div>

                            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                                <div v-if="!fetching">
                                    <div class="row justify-center items-center bg-grey-3">
                                        <div class="col-1 q-pa-md bg-grey-4">
                                            ID
                                        </div>
                                        <div class="col q-pa-sm">
                                            Target
                                        </div>
                                        <div class="col q-pa-sm">
                                            Targets
                                        </div>
                                    </div>
                                    <q-scroll-area visible style="height:30vh">
                                        <q-card v-for="insert in inserts" :key="insert.pk" flat square>
                                            <div class="row justify-center items-center bg-grey-3">
                                                <div class="col-1 q-pa-lg bg-grey-4">
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

                                            </div>
                                        </q-card>
                                    </q-scroll-area>
                                </div>
                            </transition>
                            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                        </q-card>
                    </div>
                </div>
            </q-card-section>

        </div>

    </q-card>
    <div class="absolute-bottom q-pa-sm q-mb-md">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-3 text-white" size="md" label="change settings" icon="edit" @click="editRoom" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
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

export default defineComponent({
    name: 'SettingsView',
    emits: ["back", "next"],
    beforeMount() {
        this.fetching = true
        this.getSettings()
    },
    data() {
        return {
            usingDatabase: false,

            blocks: 0,
            blocksMustAlign: false,
            classSize: 0,
            lessonCost: 0,
            maxSubjectsPerBlock: 0,
            settingsTitle: "",
            settingsId: 0,
            optionsId: 0,

            fetching: false,
            errorMessage: "",
            successMessage: "",

            inserts: []
        }
    },
    methods: {
        getSettings() {
            this.fetching = true
            axiosInstance.get(`api-rooms/rooms/${this.$route.params.room_id}/room_with_settings/`).then(
                (response) => {
                    if (response.status == 200) {
                        let data = response.data;

                        this.blocks = data.settings.blocks;
                        this.blocksMustAlign = data.settings.blocks_must_align
                        this.classSize = data.settings.class_size
                        this.lessonCost = data.settings.lesson_cost
                        this.maxSubjectsPerBlock = data.settings.max_subjects_per_block
                        this.settingsTitle = data.settings.title
                        this.settingsId = data.settings.id
                        this.optionsId = data.opts_id

                        this.inserts = data.inserts

                        this.$store.commit("setSettingsData", data)

                        this.fetching = false
                    } else {
                        this.$router.push({
                            name: "E404"
                        })
                    }
                }
            )
        },
        editRoom() {
            this.$router.push({
                "name": "room-edit",
                params: {
                    user_id: this.$route.params.user_id,
                    room_id: this.$route.params.room_id,
                }
            })
        }
    },

});
</script>
