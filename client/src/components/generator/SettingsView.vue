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
                            <div class="text-h3 text-center">Generation Settings</div>

                            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                                <div class="row q-gutter-md">
                                    <div class="col q-gutter-md">
                                        <q-input v-model="settingsTitle" autofocus outlined label="title" type="text" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="grid_view" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="blocks" autofocus outlined label="blocks" type="number" readonly>
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
                                        <q-input v-model="classSize" autofocus outlined label="class size" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="school" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number" readonly>
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>

                                    </div>
                                </div>
                            </transition>
                            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />
                        </q-card>
                    </div>

                    <div class="col">
                        <q-card class="q-pa-md bg-white" style="min-height:50vh">
                            <div class="text-h3 text-center">Rules</div>

                            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                                <div class="row q-gutter-md">
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
            blocksMustAlign: 0,
            classSize: 0,
            lessonCost: 0,
            maxSubjectsPerBlock: 0,
            settingsTitle: "",
            settingsId: 0,
            optionsId: 0,

            fetching: false,
            errorMessage: "",
            successMessage: "",
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
