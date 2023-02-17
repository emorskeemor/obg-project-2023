<template>
<q-page class="q-pa-md no-scroll" padding>
    <div class="row q-gutter-xl">
        <div class="col-4">
            <!-- Room settings. Allows the user to edit the settings of the ROOM  -->
            <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:75vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font text-weight-medium">Room Settings</div>
                </q-card-section>
                <q-card-section>
                    <div class="text-body2 q-pb-sm">
                        Room settings will be responsible for how students access the room and its identification
                    </div>
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div v-show="!fetching">
                            <div>
                                <div class="row q-gutter-sm">
                                    <div class="col">
                                        <q-input v-model="domain" autofocus outlined label="domain name" hint="domain name" :rules="[
                                val => !!val || 'A domain is required']">
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
                                    <q-toggle v-model="checkEmailDomain" label="Check domain" size="md" />

                                </div>
                                <div class="row q-ma-md">
                                    <q-input v-model="emailMatch" autofocus outlined label="email match" hint="A student's email domain must match a required room domain" :readonly="!checkEmailDomain" :rules="[
                                val => !!val || 'An email match is required']" v-if="checkEmailDomain">
                                        <template v-slot:prepend>
                                            <q-icon name="email" />
                                        </template>
                                    </q-input>
                                </div>
                                <div class="row full-width bg-grey-4 q-pa-sm">
                                    <div class="col-7">
                                        <div class="main-font text-body2 q-pa-sm">upload students' options from a csv</div>
                                        <q-file filled bottom-slots v-model="dataFile" label="upload data file" counter max-files="1" class="q-ml-md q-mb-md">

                                            <template v-slot:append>
                                                <q-icon v-if="dataFile !== null" name="close" @click.stop.prevent="dataFile = null" class="cursor-pointer" />
                                                <q-icon name="create_new_folder" @click.stop.prevent />
                                            </template>

                                            <template v-slot:hint>
                                                upload student data here
                                            </template>

                                            <template v-slot:after>
                                                <q-btn round dense flat icon="upload_file" @click="bulkCreate" />
                                            </template>
                                        </q-file>
                                    </div>
                                    <div class="col">
                                        <q-toggle v-model="dummyNames" label="dummy names" />
                                        <!-- <q-toggle v-model="useSubjectCode" label="use subject codes" /> -->
                                        <q-toggle v-model="showFailed" label="deffer failure" />
                                    </div>
                                </div>
                            </div>
                        </div>
                    </transition>

                </q-card-section>
                <div class="bg-grey-4 absolute-bottom q-pa-sm">
                    <q-btn label="Save" color="teal-4" @click="saveRoomSettings" size="md" icon="done" />
                </div>
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

            </q-card>
        </div>
        <!-- control pannel island. Shows extra utility that can be used -->
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
                        <!-- button to redirect to generation view -->
                        <q-btn label="Generate" color="blue" size="lg" @click="changeRoute('options-generator')" glossy :disable="fetching" />
                    </div>

                </q-card-section>
                <!-- utility buttons that link to other pages or popups -->
                <q-card-actions class="bg-grey-4 absolute-bottom row justify-center">
                    <div class="text-h6 row full-width justify-center q-ma-sm">Other Settings</div>
                    <div class="text-body2 full-width justify-center q-mb-md">Edit the available options, students and the generation rules</div>
                    <q-btn-group class="row">
                        <q-btn label="Options" color="teal-4" @click="editAvailableChoices" size="md" icon="subject" :disable="fetching" />
                        <q-btn label="Students" color="teal-4" @click="changeRoute('students-view')" size="md" icon="account_circle" :disable="fetching" />
                        <q-btn label="Rules" color="teal-4" @click="changeRoute('rules-edit')" size="md" icon="rule" :disable="fetching" />
                    </q-btn-group>
                    <q-btn-group class="q-mt-md">
                        <q-btn label="Room's blocks" color="teal-4" size="md" :disable="fetching" icon="grid_view" @click="displayBlocksPopup=true" />
                        <q-btn label="Your dashboard" color="teal-4" size="md" :disable="fetching" @click="returnToDashboard" icon="dashboard" />

                    </q-btn-group>

                </q-card-actions>

            </q-card>

        </div>
        <!-- Generation settings. Allows user to edit the way the algorithm generates its option blocks -->
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
                                    <!-- the title of the settings -->
                                    <div class="col">
                                        <q-input v-model="settingsTitle" autofocus outlined label="settings title" :rules="[
                                val => !!val || 'A title is required']">
                                            <template v-slot:prepend>
                                                <q-icon name="edit" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <!-- the number of blocks to be generated -->
                                    <div class="col">
                                        <q-input v-model="blocks" autofocus outlined label="blocks" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']">
                                            <template v-slot:prepend>
                                                <q-icon name="grid_view" />
                                            </template>
                                        </q-input>

                                    </div>
                                </div>
                                <div class="row q-gutter-sm">
                                    <!-- the maxium class size -->
                                    <div class="col">
                                        <q-input v-model="classSize" autofocus outlined label="class size" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']" filled>
                                            <template v-slot:prepend>
                                                <q-icon name="school" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <!-- subjects delegated to each block -->
                                    <div class="col">
                                        <q-input v-model="maxSubjectsPerBlock" autofocus outlined label="subjects per block" type="number" :rules="[val=>val > 0 || 'value must be greater than zero']" filled>
                                            <template v-slot:prepend>
                                                <q-icon name="subject" />
                                            </template>
                                        </q-input>
                                    </div>
                                </div>
                                <div class="row q-gutter-sm">
                                    <!-- lesson cost -->
                                    <div class="col">
                                        <q-input v-model="lessonCost" autofocus outlined label="lesson cost" type="number" :rules="[val=>val >= 0 || 'value must be postive or zero']">
                                            <template v-slot:prepend>
                                                <q-icon name="currency_pound" />
                                            </template>
                                        </q-input>
                                    </div>
                                    <!-- reserve options -->
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
                    <q-btn label="Save" color="teal-4" @click="saveGenerationSettings" size="md" icon="done" :disable="fetching" />
                </q-card-section>
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

            </q-card>
        </div>
    </div>
    <!-- popup to show room's blocks -->
    <q-dialog v-model="displayBlocksPopup">
        <q-card style="min-width: 60vh" class="q-pa-md">
            <q-card-section>
                <div class="text-h4 text-center main-font text-weight-medium">Room's blocks</div>
                <div class="text-body2 text-center main-font">The blocks that this room has generated will end up here when you save them</div>
            </q-card-section>
            <q-card-section class="q-gutter-md">
                <BlocksList :blocks=filteredBlocks @delete="deleteBlock" @info="displayBlockInfo" />
            </q-card-section>
            <div class="row justify-center">
                <q-pagination v-model="blockPage" :max=blocksPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />
            </div>
        </q-card>
    </q-dialog>
    <!-- display popup to show the results of a given option block -->
    <q-dialog v-model="showBlockInfo">
        <ResultsPopup :data="currentBlock" />
    </q-dialog>
    <!-- error and success banners if the saving was successful or not -->
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
import ResultsPopup from '@/components/misc/ResultsPopup.vue';
import BlocksList from '@/components/misc/BlocksList.vue';

const CHOSEN_OPTIONS_PER_PAGE = 2

export default defineComponent({
        name: "RoomEditView",
        components: {
            BannerComponent,
            ResultsPopup,
            BlocksList
        },
        data() {
            return {
                // room details
                emailMatch: "",
                title: "",
                code: "",
                domain: "",
                public: false,
                checkEmailDomain: false,
                // settings details
                blocks: 0,
                blocksMustAlign: false,
                classSize: 0,
                lessonCost: 0,
                maxSubjectsPerBlock: 0,
                settingsTitle: "",
                settingsId: 0,
                allowedReserves: 2,
                // utility
                fetching: true,
                errorMessage: "",
                successMessage: "",
                optionsId: 0,
                // dump csv of student options 
                // to the database
                dataFile: ref(null),
                dummyNames: true,
                useSubjectCode: true,
                showFailed: false,
                // used for showing blocks linked
                // to this room
                displayBlocksPopup: false,
                roomBlocks: [],
                currentBlock: [],
                showBlockInfo: false,
                blockPage: 1,
                blockSearch: "",

            }
        },
        beforeMount() {
            this.fetchSettings()
        },
        computed: {

            blocksPagination() {
                return Math.floor(this.roomBlocks.length / CHOSEN_OPTIONS_PER_PAGE) + 1

            },
            filteredBlocks() {
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
            displayBlockInfo(block) {
                // display popup about a certain set of blocks that were evaluated
                this.currentBlock = block
                this.showBlockInfo = true
            },
            // FETCHING METHODS
            deleteBlock(block) {
                // delete a given set of option blocks
                axiosInstance.delete(`api-generate/option-blocks/${block.id}`).then(
                    () => {
                        this.fetchSettings()
                    })
            },
            fetchSettings() {
                this.clearMessages()
                this.fetching = true
                axiosInstance.get(`api-rooms/rooms/${this.$route.params.room_id}/room-with-settings/`).then(
                    (response) => {
                        if (response.status == "200") {
                            let data = response.data;
                            // data for room
                            this.title = data.room.title
                            this.code = data.room.code;
                            this.domain = data.room.domain;
                            this.public = data.room.public;
                            this.emailMatch = data.room.email_domain
                            this.checkEmailDomain = data.room.check_email_domain
                            // data for settings
                            this.blocks = data.settings.blocks;
                            this.blocksMustAlign = data.settings.blocks_must_align
                            this.classSize = data.settings.class_size
                            this.lessonCost = data.settings.lesson_cost
                            this.maxSubjectsPerBlock = data.settings.max_subjects_per_block
                            this.settingsTitle = data.settings.title
                            this.settingsId = data.settings.id
                            this.optionsId = data.opts_id
                            // blocks connected to this room
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
            saveRoomSettings() {
                this.clearMessages()
                if (this.checkAllNotEmpty(
                        [this.domain, this.title, this.emailMatch]
                    ) === false) {
                    this.errorMessage = "please fix any outstanding errors"
                } else {
                    // save room settings
                    axiosInstance.put(`api-rooms/rooms/${this.$route.params.room_id}/`, {
                        domain: this.domain,
                        title: this.title,
                        public: this.public,
                        check_email_domain: this.checkEmailDomain,
                        email_domain: this.emailMatch
                    }).then(() => {
                        this.successMessage = "Saving room settings was successful"
                    }).catch(() => {
                        this.errorMessage = "Error while saving generation settings"
                    })
                }
            },
            saveGenerationSettings() {
                this.clearMessages()
                // save generation settings
                if (this.checkAllNumbers(
                        [this.blocks, this.classSize, this.allowedReserves, this.maxSubjectsPerBlock]
                    ) === false | this.emptyCheck(this.settingsTitle) == true | this.lessonCost < 0) {
                    this.errorMessage = "please fix any outstanding errors"
                } else {
                    axiosInstance.put(`api-rooms/settings/${this.settingsId}/`, {
                        title: this.settingsTitle,
                        blocks_must_align: this.blocksMustAlign,
                        max_subjects_per_block: this.maxSubjectsPerBlock,
                        blocks: this.blocks,
                        class_size: this.classSize,
                        lesson_cost: this.lessonCost
                    }).then(() => {
                        this.successMessage = "Saving generation settings was successful"
                    }).catch(() => {
                        this.errorMessage = "Error while saving generation settings"
                    })
                }
            },
            deleteAllStudent() {
                // deletes all students
                this.clearMessages()
                this.fetching = true
                axiosInstance.delete(`api-rooms/rooms/${this.$route.params.room_id}/delete-all-students/`).then(
                    () => {
                        this.successMessage = "all students connected to this room have been deleted"
                        this.fetching = false
                    }
                )
            },
            bulkCreate() {
                this.clearMessages()
                // bulk create students from a csv file
                this.fetching = true
                var formData = new FormData()
                formData.append("data", this.dataFile)
                // payload data to send
                const payload = {
                    "data_using_csv": true,
                    "room_code": this.$route.params.room_id,
                    "options_using": this.settingsTitle,
                    "allowed_reserves": this.allowedReserves,
                    "max_opts_per_student": this.blocks,
                    "generate_dummy_names": this.dummyNames,
                    "show_failed": this.showFailed,
                    "use_subject_code": this.useSubjectCode

                }
                formData.append("payload", JSON.stringify(payload))
                // send the data
                axiosInstance.post(`api-students/students/dump-students/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }).then(
                    () => {
                        this.successMessage = "student options have been saved to the database"
                        this.fetching = false
                    }
                ).catch(err=>{
                    this.errorMessage = err.response.data.detail
                    this.fetching = false
                })
            },
            // REDIRECT METHODS

            changeRoute(route) {
                // general route change
                this.$router.push({
                    name: route,
                    params: {
                        user_id: this.$route.params.user_id,
                        room_id: this.$route.params.room_id,
                    }
                })
            },
            editAvailableChoices() {
                // redirect to edit available option choices for this room
                this.$router.push({
                    name: "available-opts-edit",
                    params: {
                        user_id: this.$route.params.user_id,
                        room_id: this.$route.params.room_id,
                        opts_id: this.optionsId
                    }
                })
            },
            returnToDashboard() {
                // redirect to user dashboard
                this.$router.push({
                    name: "user-dashboard",
                    params: {
                        user_id: this.$route.params.user_id
                    }
                })
            },
            // UTILTIY METHODS
            checkAllNumbers(items) {
                for (let i = 0; i < items.length; i++) {
                    if (items[i] <= 0) {
                        return false
                    }
                }
                return true
            },
            checkAllNotEmpty(items) {
                for (let i = 0; i < items.length; i++) {
                    if (items[i].length === 0) {
                        return false
                    }
                }
                return true
            },
            zeroCheck(value) {
                return value <= 0
            },
            emptyCheck(value) {
                return value.length == 0
            },
            clearMessages() {
                this.errorMessage = ""
                this.successMessage = ""
            }

        }
    },

)
</script>
