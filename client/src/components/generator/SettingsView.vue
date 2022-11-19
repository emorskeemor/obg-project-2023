<template>
<div style="min-height:63vh">
    <q-card class="absolute-center bg-grey-3" style="width:100%;height:80%;" square>
        <div class="q-pa-md">
            <q-card-section>
                <div class="text-h3">
                    Ensure your settings are go to go
                </div>
            </q-card-section>
            <div class="row q-gutter-xl">
                <div class="col">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div v-if="!fetching">
                            <q-card class="q-pa-md bg-white">
                                <div class="row q-gutter-md">
                                    <div class="col q-gutter-md">
                                        <q-input v-model="blocks" autofocus outlined label="blocks" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="grid_view" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="currency_pound" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <div class="col q-gutter-md">
                                        <q-input v-model="classSize" autofocus outlined label="class size" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="school" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>

                                    </div>
                                </div>
                            </q-card>
                        </div>
                    </transition>
                </div>

                <div class="col">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div v-if="!fetching">
                            <q-card class="q-pa-md bg-white">
                                <div class="row q-gutter-md">
                                    <div class="col q-gutter-md">
                                        <q-input v-model="blocks" autofocus outlined label="blocks" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="grid_view" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="currency_pound" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <div class="col q-gutter-md">
                                        <q-input v-model="classSize" autofocus outlined label="class size" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="school" />
                                            </template>
                                        </q-input>
                                        <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number">
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>

                                    </div>
                                </div>
                            </q-card>
                        </div>
                    </transition>
                </div>
            </div>

        </div>

    </q-card>
    <div class="absolute-bottom-left q-pa-sm">
        <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
    </div>
</div>
</template>

<script lang="ts">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';

export default defineComponent({
    name: 'OptionsProivsionsView',
    emits: ["choose", "back"],
    watch: {
        file() {
            this.$emit("choose", this.file)
        }
    },
    beforeMount() {
        this.fetching = true
        this.getSettings()
    },
    data() {
        return {
            label: ref("hello"),
            file: ref(null),
            usingDatabase: false,

            blocks: 0,
            blocksMustAlign: 0,
            classSize: 0,
            lessonCost: 0,
            maxSubjectsPerBlock: 0,
            settingsTitle: 0,
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

                        this.fetching = false
                    } else {
                        this.$router.push({
                            name: "E404"
                        })
                    }
                }
            )
        },
    }

});
</script>
