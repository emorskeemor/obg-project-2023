<template>
<q-page class="q-pa-xs no-scroll" padding>
    <!-- current rooms  -->
    <div class="q-pa-md" style="width:100%">
        <div class="row q-gutter-xl">
            <div class="col-4">
                <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:75vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font text-weight-medium">Room Settings</div>
                    </q-card-section>
                    <q-card-section>
                        <div class="text-body2">
                            Room settings will be responsible for how students access the room and its identification
                        </div>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching">
                                <div>
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
                                    <div class="row q-ma-md">
                                        <q-input v-model="emailMatch" autofocus outlined label="email match" hint="A student's email domain must match a required room domain" :readonly="!CheckEmailDomain">
                                            <template v-slot:prepend>
                                                <q-icon name="email" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <!-- <div class="row q-gutter-sm q-ma-md">
                                        <q-btn press color="red-7 glossy" label="remove all students" @click="deleteAllStudent" size="sm" />

                                    </div> -->
                                    <div class="row full-width bg-grey-4 q-pa-sm">
                                        <div class="col-7">
                                            <div class="main-font text-body2 q-pa-sm">upload students' options from a csv</div>
                                            <q-file filled bottom-slots v-model="dataFile" label="upload data file" counter max-files="1" class="q-ml-md">

                                                <template v-slot:append>
                                                    <q-icon v-if="dataFile !== null" name="close" @click.stop.prevent="dataFile = null" class="cursor-pointer" />
                                                    <q-icon name="create_new_folder" @click.stop.prevent />
                                                </template>

                                                <template v-slot:hint>
                                                    Field hint
                                                </template>

                                                <template v-slot:after>
                                                    <q-btn round dense flat icon="upload_file" @click="bulkCreate" />
                                                </template>
                                            </q-file>
                                        </div>
                                        <div class="col">
                                            <q-toggle v-model="dummyNames" label="dummy names" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </transition>

                    </q-card-section>
                    <div class="bg-grey-4 absolute-bottom q-pa-sm">
                        <q-btn label="Save" color="teal-4" @click="saveRoom" size="md" icon="done" />
                    </div>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <!-- middle column -->
            <div class="col">
                <q-card class="bg-grey-3 shadow-15" style="min-height:70vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font text-weight-medium">Room Details</div>
                        <div class="q-pa-md">
                            <q-input v-model="code" autofocus outlined label="room code" hint="code of the room" readonly>
                                <template v-slot:prepend>
                                    <q-icon name="vpn_key" />
                                </template>
                            </q-input>
                        </div>
                    </q-card-section>
                    <q-card-section class="row justify-center items-center">
                        <div>
                            Here you can edit this room and the settings that are attatched to it
                        </div>
                        <div class="row justify-center q-pa-sm">
                            <q-btn label="Generate" color="blue" size="lg" @click="changeRoute('options-generator')" glossy :disable="fetching" />
                        </div>

                    </q-card-section>

                    <q-card-actions class="bg-grey-4 absolute-bottom row justify-center">
                        <div class="text-h6 row full-width justify-center q-ma-sm">Other Settings</div>
                        <div class="text-body2 full-width justify-center q-mb-md">Edit the available options, students and the generation rules</div>
                        <q-btn-group class="row">
                            <q-btn label="Options" color="teal-4" @click="editAvailableChoices" size="md" icon="subject" :disable="fetching" />
                            <q-btn label="Students" color="teal-4" @click="changeRoute('students-view')" size="md" icon="account_circle" :disable="fetching" />
                            <q-btn label="Rules" color="teal-4" @click="changeRoute('rules-edit')" size="md" icon="rule" :disable="fetching" />
                        </q-btn-group>
                        <q-btn-group class="q-mt-md">
                            <q-btn label="Room's blocks" color="teal-3" size="md" :disable="fetching" icon="grid_view" @click="displayBlocksPopup=true" />
                            <q-btn label="Your dashboard" color="teal-3" size="md" :disable="fetching" @click="returnToDashboard" icon="dashboard" />

                        </q-btn-group>

                    </q-card-actions>

                </q-card>

            </div>
            <!-- generated blocks -->
            <div class="col-4">
                <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:75vh">
                    <q-card-section class="bg-grey-4">
                        <div class="text-h4 main-font text-weight-medium">Generation Settings</div>
                    </q-card-section>
                    <q-card-section>
                        <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                            <div v-show="!fetching">
                                <div class="q-gutter-md q-pa-sm">
                                    <div class="text-body2">
                                        Settings will be responsible for how the option blocks are generated
                                    </div>

                                    <div class="row q-gutter-sm">
                                        <div class="col">
                                            <q-input v-model="settingsTitle" autofocus outlined label="settings title">
                                                <template v-slot:prepend>
                                                    <q-icon name="edit" />
                                                </template>
                                            </q-input>
                                        </div>
                                        <div class="col">
                                            <q-input v-model="blocks" autofocus outlined label="blocks" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']">
                                                <template v-slot:prepend>
                                                    <q-icon name="grid_view" />
                                                </template>
                                            </q-input>

                                        </div>
                                    </div>
                                    <div class="row q-gutter-sm">
                                        <div class="col">
                                            <q-input v-model="classSize" autofocus outlined label="class size" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']">
                                                <template v-slot:prepend>
                                                    <q-icon name="school" />
                                                </template>
                                            </q-input>
                                        </div>
                                        <div class="col">
                                            <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']">
                                                <template v-slot:prepend>
                                                    <q-icon name="subject" />
                                                </template>
                                            </q-input>
                                        </div>
                                    </div>
                                    <div class="row q-gutter-sm">
                                        <div class="col">
                                            <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number" :rules="[val=>val >= 0 || 'value must be postive or zero']">
                                                <template v-slot:prepend>
                                                    <q-icon name="currency_pound" />
                                                </template>
                                            </q-input>
                                        </div>
                                        <div class="col">
                                            <q-input v-model="allowedReserves" autofocus outlined label="allowed reserves" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']">
                                                <template v-slot:prepend>
                                                    <q-icon name="subject" />
                                                </template>
                                            </q-input>
                                        </div>
                                    </div>
                                    <div class="row q-gutter-sm">
                                        <q-toggle v-model="blocksMustAlign" label="blocks must align" />
                                    </div>
                                </div>
                            </div>
                        </transition>

                    </q-card-section>
                    <q-card-section class="bg-grey-4 absolute-bottom">
                        <q-btn label="Save" color="teal-4" @click="saveSettings" size="md" icon="done" :disable="fetching" />
                    </q-card-section>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
        </div>
    </div>
    <!-- room's blocks -->
    <q-dialog v-model="displayBlocksPopup">
        <q-card style="min-width: 60vh" class="q-pa-md">
            <q-card-section>
                <div class="text-h4 text-center">Room's blocks</div>
            </q-card-section>

            <q-card-section class="q-gutter-md">
                <div v-for="block in getFilteredBlocks" :key="block.id">
                    <div class="row justify-center items-center">
                        <q-card style="width:55vh;margin:1vh" class="bg-teal-3 glossy">
                            <q-card-section>
                                <div class="text-h5 text-white">{{block.title}}/{{block.room.code}}</div>
                            </q-card-section>
                            <q-card-actions>
                                <q-btn class="bg-blue-grey text-white" icon="highlight_off" @click="deleteBlock(block)" />
                                <q-btn class="bg-blue text-white" icon="info" @click="blockInfo(block)" />
                            </q-card-actions>
                        </q-card>
                    </div>
                </div>
            </q-card-section>
            <q-pagination v-model="blockPage" :max=blocksPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />

        </q-card>
    </q-dialog>
    <q-dialog v-model="showBlockInfo">
        <q-card style="min-width: 100vh" class="q-pa-md">
            <div class="text-h5 text-center main-font text-weight-medium">{{ currentBlock.title }}/{{ currentBlock.room.code }}
                
            </div>
            <div class="row">
                <q-chip icon="grid_view"># blocks : {{ currentBlock.number_of_blocks }}</q-chip>
                <q-chip icon="done">success % : {{ currentBlock.success_percentage }}</q-chip>
                <q-chip icon="category">completed nodes : {{ currentBlock.completed_nodes }}</q-chip>
                <q-chip icon="category">generated nodes : {{ currentBlock.generated_nodes }}</q-chip>
                <q-chip icon="schedule">generation time : {{ currentBlock.generation_time }} seconds</q-chip>
            </div>
            <q-card-section class="q-gutter-md">
                <q-scroll-area style="height:75vh">
                    <q-card square class="q-pa-md bg-grey-4" flat>
                        <div class="row justify-center">
                            <div v-for="(block, index) in currentBlock.blocks" :key="index">
                                <q-card style="width:80vh;min-height:15vh">
                                    <div class="row">
                                        <div class="col bg-grey-3" style="min-height:15vh">
                                            <div class="text-h6 text-black q-pa-sm row">Block<div class="text-bold q-ml-sm">[{{index+1}}] </div>
                                                <q-chip icon="subject">{{ block.length }}</q-chip>
                                            </div>
                                        </div>
                                        <div class="col-10">
                                            <div class="row q-pa-sm">
                                                <div v-for="code in block" :key="code" style="padding:5px">
                                                    <q-card class="bg-grey-2" style="padding:3px">
                                                        <div class="text-black main-font">{{code[0]}} {{ code[1] }}</div>

                                                    </q-card>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </q-card>
                            </div>
                        </div>
                    </q-card>
                </q-scroll-area>
            </q-card-section>

        </q-card>
    </q-dialog>
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
const CHOSEN_OPTIONS_PER_PAGE = 2

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
                blocksMustAlign: false,
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
                allowedReserves: 2,
                dummyNames: true,
                displayBlocksPopup: false,
                roomBlocks: [],
                currentBlock: [],
                showBlockInfo: false,
                blockPage: 1,
                blockSearch: "",

            }
        },
        beforeMount() {
            this.getSettings()
        },
        computed: {

            blocksPagination() {
                return Math.floor(this.roomBlocks.length - 1 / CHOSEN_OPTIONS_PER_PAGE)

            },
            getFilteredBlocks() {
                // get chosen options through the search
                if (this.fetching) {
                    return []
                } else {

                    let startingPage = (this.blockPage - 1) * CHOSEN_OPTIONS_PER_PAGE
                    return [...[...this.roomBlocks].filter(
                        block => block.title.toLowerCase().includes(this.blockSearch.toLowerCase())
                    )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
                }
            },
        },
        methods: {
            deleteBlock(block) {
                // delete a given room
                axiosInstance.delete(`api-generate/option-blocks/${block.id}`).then(
                    response => {
                        this.getSettings()
                    })
            },
            blockInfo(block) {
                this.currentBlock = block
                this.showBlockInfo = true
            },
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

                            this.roomBlocks = data.blocks

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
            changeRoute(route) {
                this.$router.push({
                    name: route,
                    params: {
                        user_id: this.$route.params.user_id,
                        room_id: this.$route.params.room_id,
                    }
                })
            },
            deleteAllStudent() {
                this.fetching = true
                axiosInstance.delete(`api-rooms/rooms/${this.$route.params.room_id}/delete-all-students/`).then(
                    response => {
                        console.log(response);
                        this.fetching = false
                    }
                )
            },
            bulkCreate() {
                this.fetching = true
                var formData = new FormData()
                formData.append("data", this.dataFile)
                const payload = {
                    "data_using_csv": true,
                    "room_code": this.$route.params.room_id,
                    "options_using": this.settingsTitle,
                    "allowed_reserves": this.allowedReserves,
                    "max_opts_per_student": this.blocks,
                    "generate_dummy_names": this.dummyNames

                }
                formData.append("payload", JSON.stringify(payload))

                axiosInstance.post(`api-students/students/dump-students/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }).then(
                    response => {
                        console.log(response);
                        this.fetching = false
                    }
                )
            },
            returnToDashboard() {
                this.$router.push({
                    name: "user-dashboard",
                    params: {
                        user_id: this.$route.params.user_id
                    }
                })
            }
        }
    },

)
</script>
