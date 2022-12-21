<template>
<q-page class="q-pa-xs no-scroll" padding>
    <!-- current rooms  -->
    <div class="q-pa-md" style="width:100%">
        <div class="row q-gutter-xl">
            <div class="col-4">
                <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font">Room Settings</div>
                    </q-card-section>
                    <q-card-section>
                        <div class="text-body2">
                            Room settings will be responsible for how students access the room and its identification
                        </div>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching">
                                <div class="q-gutter-md q-pa-sm">
                                    <div class="row q-gutter-sm">
                                        <div class="col">
                                            <q-input v-model="domain" autofocus outlined label="domain name" hint="domain name">
                                                <template v-slot:prepend>
                                                    <q-icon name="domain" />
                                                </template>
                                            </q-input>
                                        </div>
                                        <div class="col">
                                            <q-input v-model="title" autofocus outlined label="room title" :rules="[
                                val => !!val || 'A title is required']">
                                                <template v-slot:prepend>
                                                    <q-icon name="house" />
                                                </template>
                                            </q-input>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <q-toggle v-model="public" label="Public" size="md" />
                                        <q-toggle v-model="CheckEmailDomain" label="Check domain" size="md" />

                                    </div>
                                    <div class="row">
                                        <q-input v-model="emailMatch" autofocus outlined label="email match" hint="A student's email domain must match a required room domain" :readonly="!CheckEmailDomain">
                                            <template v-slot:prepend>
                                                <q-icon name="email" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <div class="row q-gutter-sm">
                                        <q-btn press color="red" label="remove all students" @click="deleteAllStudent" size="sm" />

                                    </div>
                                    <div class="row">
                                        <div class="col-7">
                                            <q-file filled bottom-slots v-model="dataFile" label="upload data file" counter max-files="12">

                                                <template v-slot:append>
                                                    <q-icon v-if="dataFile !== null" name="close" @click.stop.prevent="dataFile = null" class="cursor-pointer" />
                                                    <q-icon name="create_new_folder" @click.stop.prevent />
                                                </template>

                                                <template v-slot:hint>
                                                    Field hint
                                                </template>

                                                <template v-slot:after>
                                                    <q-btn round dense flat icon="upload_file" @click="bulkCreate"/>
                                                </template>
                                            </q-file>
                                        </div>
                                        <div class="col">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </transition>

                    </q-card-section>
                    <q-card-section class="bg-grey-4 absolute-bottom">
                        <q-btn label="Save" color="teal-4" @click="saveRoom" size="md" icon="done" />
                    </q-card-section>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <!-- middle column -->
            <div class="col">
                <q-card class="bg-grey-3" style="min-height:70vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h3 main-font">Room Details</div>
                        <div class="q-pa-md">
                            <q-input v-model="code" autofocus outlined label="room code" hint="code of the room" readonly>
                                <template v-slot:prepend>
                                    <q-icon name="vpn_key" />
                                </template>
                            </q-input>
                        </div>
                    </q-card-section>
                    <q-card-section>
                        <div>
                            Here you can edit this room and the settings that are attatched to it
                        </div>
                    </q-card-section>

                    <q-card-section class="bg-grey-4 absolute-bottom">
                        <q-btn label="Generate" color="red-7" size="lg" @click="generatorView" glossy />
                    </q-card-section>
                    <q-card-section class="bg-grey-4">
                        <div class="text-h5 q-pa-xs">Available options</div>
                        <div class="text-body2 q-mb-md">Edit the available options for the room</div>
                        <div class="text-h4 main-font"></div>
                        <q-btn label="Edit" color="teal-4" @click="editAvailableChoices" size="md" icon="edit" />

                    </q-card-section>

                </q-card>

            </div>
            <!-- generated blocks -->
            <div class="col-4">
                <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font">Generation Settings</div>
                    </q-card-section>
                    <q-card-section>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching">
                                <div class="q-gutter-md q-pa-sm">
                                    <div class="text-body2">
                                        Settings will be responsible for how the option blocks are generated
                                    </div>

                                    <q-input v-model="settingsTitle" autofocus outlined label="settings title">
                                        <template v-slot:prepend>
                                            <q-icon name="edit" />
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
    <BannerComponent colour="green" :message="successMessage" @dismiss="this.successMessage=''" v-if="successMessage.length !== 0" />
    <BannerComponent colour="red" :message="errorMessage" @dismiss="this.errorMessage=''" v-if="errorMessage.length !== 0" />
</q-page>
<div>

</div>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    ref,
    defineComponent
} from 'vue';
import BannerComponent from '@/components/misc/BannerComponent.vue';

export default defineComponent({
        name: "RoomEditView",
        components: {
            BannerComponent,
        },
        data() {
            return {
                // room details
                emailMatch: "",
                title: "",
                code: "",
                domain: "",
                public: false,
                CheckEmailDomain: false,
                // settings details
                blocks: 0,
                blocksMustAlign: 0,
                classSize: 0,
                lessonCost: 0,
                maxSubjectsPerBlock: 0,
                settingsTitle: 0,
                settingsId: 0,

                fetching: true,
                errorMessage: "",
                successMessage: "",

                optionsId: 0,

                dataFile: ref(null),
            }
        },
        beforeMount() {
            this.getSettings()
        },
        methods: {
            getSettings() {
                this.fetching = true
                axiosInstance.get(`api-rooms/rooms/${this.$route.params.room_id}/room_with_settings/`).then(
                    (response) => {
                        if (response.status == "200") {
                            let data = response.data;
                            this.title = data.room.title
                            this.code = data.room.code;
                            this.domain = data.room.domain;
                            this.public = data.room.public;
                            this.emailMatch = data.room.email_domain
                            this.CheckEmailDomain = data.room.check_email_domain

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
            saveRoom() {
                axiosInstance.put(`api-rooms/rooms/${this.$route.params.room_id}/`, {
                    domain: this.domain,
                    title: this.title,
                    public: this.public,
                    check_email_domain: this.CheckEmailDomain,
                    email_domain: this.emailMatch
                }).then(res => {
                    if (res.status == "200") {
                        this.successMessage = "save success"
                        this.errorMessage = ""
                    } else {
                        this.errorMessage = "save unsuccessful"
                        this.successMessage = ""
                    }
                })
            },
            saveSettings() {
                axiosInstance.put(`api-rooms/settings/${this.settingsId}/`, {
                    title: this.settingsTitle,
                    blocks_must_align: this.blocksMustAlign,
                    max_subjects_per_block: this.maxSubjectsPerBlock,
                    blocks: this.blocks,
                    class_size: this.classSize,
                    lesson_cost: this.lessonCost
                }).then(res => {
                    if (res.status == "200") {
                        this.successMessage = "save success"
                        this.errorMessage = ""
                    } else {
                        this.errorMessage = "save unsuccessful"
                        this.successMessage = ""
                    }
                })
            },
            editAvailableChoices() {
                this.$router.push({
                    name: "available-opts-edit",
                    params: {
                        user_id: this.$route.params.user_id,
                        room_id: this.$route.params.room_id,
                        opts_id: this.optionsId
                    }
                })
            },
            generatorView() {
                this.$router.push({
                    name: "options-generator",
                    params: {
                        user_id: this.$route.params.user_id,
                        room_id: this.$route.params.room_id,
                    }
                })
            },
            deleteAllStudent() {
                axiosInstance.delete(`api-rooms/rooms/${this.$route.params.room_id}/delete-all-students/`).then(
                    response => {
                        console.log(response);
                    }
                )
            },
            bulkCreate() {
                var formData = new FormData()
                formData.append("data", this.dataFile)
                const payload = {
                    "data_using_csv": true,
                    "room_code": this.$route.params.room_id,
                    "options_using": this.settingsTitle

                }
                formData.append("payload", JSON.stringify(payload))

                axiosInstance.post(`api-students/students/dump-students/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }).then(
                    response => {
                       console.log(response);
                    }
                )
            }
        }
    },

)
</script>
