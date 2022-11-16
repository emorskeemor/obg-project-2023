<template>
<q-page class="absolute-center" padding style="width:100%">

    <!-- current rooms  -->
    <div class="row q-gutter-xl">
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">Room Details</div>
                </q-card-section>
                <q-card-section>
                    <div class="q-gutter-md">
                        <q-input v-model="code" autofocus outlined label="room code" hint="code of the room">
                            <template v-slot:prepend>
                                <q-icon name="vpn_key" />
                            </template>
                        </q-input>
                        <q-input v-model="domain" autofocus outlined label="domain name" hint="domain name">
                            <template v-slot:prepend>
                                <q-icon name="domain" />
                            </template>
                        </q-input>

                    </div>

                </q-card-section>
                <q-card-section class="bg-grey-4 absolute-bottom">
                    <q-btn label="Save" color="green" />
                </q-card-section>
            </q-card>
        </div>
        <!-- middle column -->
        <div class="col">
            <q-card class="bg-grey-3" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font"></div>
                </q-card-section>
                <q-card-section class="bg-grey-4 absolute-bottom">
                    <div class="text-h4 main-font"></div>
                </q-card-section>
            </q-card>
        </div>
        <!-- generated blocks -->
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">Generated blocks</div>
                </q-card-section>
                <q-card-section>
                    <div class="q-gutter-md">
                        <q-input v-model="settingsTitle" autofocus outlined label="settings title">
                            <template v-slot:prepend>
                                <q-icon name="edit"/>
                            </template>
                        </q-input>
                        <q-input v-model="blocks" autofocus outlined label="blocks" type="number">
                            <template v-slot:prepend>
                                <q-icon name="grid_view" />
                            </template>
                        </q-input>
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
                        <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number">
                            <template v-slot:prepend>
                                <q-icon name="currency_pound" />
                            </template>
                        </q-input>
                    </div>
                </q-card-section>
            </q-card>
        </div>
    </div>
</q-page>
<div>

</div>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent
} from 'vue';

export default defineComponent({
        name: "RoomEditView",
        data() {
            return {
                // room details
                code: "",
                domain: "",
                public: "",
                // settings details
                blocks: 0,
                blocksMustAlign: 0,
                classSize: 0,
                lessonCost: 0,
                maxSubjectsPerBlock: 0,
                settingsTitle: 0,
            }
        },
        beforeMount() {
            this.getSettings()
        },
        methods: {
            getSettings() {
                axiosInstance.get(`api-rooms/rooms/${this.$route.params.room_id}/room_with_settings/?domain=${this.$route.params.domain}`).then(
                    (response) => {
                        let data = response.data;
                        this.code = data.room.code;
                        this.domain = data.room.domain;
                        this.public = data.room.public;
                        console.log(response);
                        this.blocks = data.settings.blocks;
                        this.blocksMustAlign = data.settings.blocks_must_align
                        this.classSize = data.settings.class_size
                        this.lessonCost = data.settings.lesson_cost
                        this.maxSubjectsPerBlock = data.settings.max_subjects_per_block
                        this.settingsTitle = data.settings.title
                    }
                )
            },
            // saveSettings() {

            // }
        }
    },

)
</script>
