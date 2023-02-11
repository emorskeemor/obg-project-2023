<template>
<q-page class="q-pa-xs no-scroll" padding>
    <div class="row q-gutter-xl q-pa-md">

        <!-- available options that the student can choose from -->

        <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 text-black main-font q-pa-md text-weight-medium">Available options</div>
                    <!-- search bar -->
                    <q-input filled v-model="availableOptionsSearch" label="Search available options" lazy-rules type="text" :disable="availableOptions.length==0">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <!-- available options draggable zone -->
                <draggable v-if="!fetching" class="list-group" :list="getFilteredAOptions" :group="{name:'availableOptions', pull:true, put:false}" itemKey="title" :move="checkMoveOption" id="availableOptions" @change="changeAvailableOptions">
                    <!-- iterate over all available options in pagination -->
                    <template #item="{element}">
                        <AvailableOptionItem :element="element" @showInfo="loadSubjectInfo" />
                    </template>
                </draggable>

                <!-- display a message to display if no searched pages are found -->
                <div v-if="getFilteredAOptions.length <= 0 && !fetching && availableOptions.length != 0">
                    <q-card class="bg-grey-5 rounded-borders" style="padding:5vh;margin:3vh">
                        <div class="text-h4 text-black main-font">Whoopsie!</div>
                        <div class="text-h6">We could not find the subject you are looking for.</div>
                    </q-card>
                </div>
                <div v-if="getFilteredAOptions.length <= 0 && !fetching && availableOptions.length == 0">
                    <q-card class="bg-grey-5 rounded-borders" style="padding:5vh;margin:3vh">
                        <div class="text-h4 text-black main-font">There is no more!</div>
                        <div class="text-h6">There are no more subjects which you can choose</div>
                    </q-card>
                </div>

                <!-- display a skeleton if the options have not yet loaded -->
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                <!-- pagination  -->
                <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                    <q-pagination v-model="availableOptionsPage" :max=getFAMPagination :max-pages=5 direction-links push color="teal" active-design="push" active-color="red-5" />
                </div>

            </q-card>

        </div>
        <!-- details about the option block choice -->

        <div class="col">
            <q-card class="bg-grey-3" style="padding:20px;min-height:75vh">
                <!-- details about how to choose the options -->
                <div class="text-h4 maint-font text-weight-bold">Room Options</div>
                <q-separator color="black" spaced />

                <div class="text-body1"><b>Drag</b> the subjects you would like to take into the chosen subjects section to the <b>right</b></div>

                <div class="text-body1 q-mt-md">These subjects on the right will be available to the students and will be used during generation</div>
                <div class="text-body1 q-mt-md">
                    <div class="text-weight-bold">Use all</div> will make all the possible option choices available to the students
                </div>
                <q-btn class="bg-teal-4 text-white" size="md" label="use all" @click="useAllSubjects" icon-right="arrow_forwards" :disable="availableOptions.length==0" />

                <div class="text-body1 q-mt-md">
                    <div class="text-weight-bold">Remove all</div> will make remove all the possible option choices available to the students
                </div>
                <q-btn class="bg-red text-white" size="md" label="remove all" @click="removeAllSubjects" icon="arrow_backwards" :disable="chosenOptions.length==0" />

                <div class="absolute-bottom justify-center bg-grey-4" style="padding:5px">
                    <q-btn-group>
                        <q-btn class="bg-teal-4 text-white" size="md" label="Save" @click="saveChoices" :disable="chosenOptions.length==0" />
                    </q-btn-group>
                </div>
            </q-card>
        </div>

        <!-- The chosen options the student has chosen -->
        <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
                <q-card-section class="bg-grey-4">
                    <q-badge color="red-12 row justify-center rounded-borders" floating rounded style="width:4vh;height:4vh">
                        <div class="text-h5 text-white">{{chosenOptions.length}}</div>
                    </q-badge>
                    <div class="text-h4 text-black main-font q-pa-md text-weight-medium">Chosen options</div>
                    <q-input filled v-model="chosenOptionsSearch" label="Search chosen options" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <draggable class="list-group" :list="getFilteredCOptions" :group="{name:'chosenOptions', pull:true, put:true}" @change="appendToChosenOptions" itemKey="name" id="chosenOptions">
                    <template #item="{element}">
                        <div class="row justify-center items-center">
                            <q-card style="width:55vh;margin:4px;max-height:15vh;" class="bg-teal-3">
                                <q-card-section style="padding:5px">
                                    <div class="text-h5 text-white">{{element.original}}, {{ element.subject_code }}</div>
                                </q-card-section>
                                <q-card-actions>
                                    <div class="row full-width items-center justify-center q-gutter-md">
                                        <div class="col q-ml-sm">
                                            <q-input standout outlined filled label="classes" v-model="element.classes" clear-icon="close" type="number" dense :rules="[ val => val > 0|val === null|val==='' || 'classes must be greater than 0']" />
                                                
                                            </div>
                                        <div class="col q-ml-sm">
                                            <q-input standout outlined filled label="title" v-model="element.title" clear-icon="close" type="text" dense :rules="[ val => val.length > 0|val === null || 'classes must be greater than 0']" />
                                                
                                            </div>
                                        <div class="col-3 q-mb-md">
                                            <q-btn-group>
                                                <q-btn class="bg-blue-grey text-white" @click="removeChosenOption(element)" icon="highlight_off" />
                                                <q-btn class="bg-blue text-white" @click="displaySubjectDetails(element)" icon="info" />
                                            </q-btn-group>
                                        </div>

                                    </div>

                                </q-card-actions>
                            </q-card>
                        </div>
                    </template>

                </draggable>
                <!-- display a skeleton if the options have not yet loaded -->
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                <!-- display a box to indicate where to place the subject -->
                <div v-if="chosenOptions.length == 0 && !fetching">
                    <q-card class="bg-grey-4 rounded-borders" style="padding:1vh;margin-inline:3vh;margin-top: 10px;">
                        <div class="text-h5 text-black main-font">Drag in an option <div class="text-weight-bold">above</div> this box</div>
                    </q-card>
                </div>
                <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                </div>
                <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                    <q-pagination v-model="chosenOptionsPage" :max=getFOMPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />
                </div>
                <div v-if="getFilteredCOptions.length == 0 && !fetching && chosenOptionsSearch.length != 0">
                    <q-card class="bg-grey-5 rounded-borders" style="padding:5vh;margin:3vh">
                        <div class="text-h4 text-black main-font">Whoopsie!</div>
                        <div class="text-h6">We could not find the subject you are looking for.</div>
                    </q-card>
                </div>
            </q-card>
        </div>
    </div>

    <BannerComponent colour="green" :message="successMessage" @dismiss="this.successMessage=''" v-if="successMessage.length !== 0" />
    <BannerComponent colour="red" :message="errorMessage" @dismiss="this.errorMessage=''" v-if="errorMessage.length !== 0" />
    <q-dialog v-model="displaySubjectInfo">
        <SubjectInfoDialog :details="displaySubjectDetails" />
    </q-dialog>
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
import SubjectInfoDialog from '@/components/options/SubjectInfoDialog.vue';

import draggable from "vuedraggable";

const AVAILABLE_OPTIONS_PER_PAGE = 5
const CHOSEN_OPTIONS_PER_PAGE = 3

export default defineComponent({
    name: 'StudentChoices',
    components: {
        draggable,
        BannerComponent,
        AvailableOptionItem,
        SubjectInfoDialog,
    },
    display: "Custom Clone",
    order: 3,
    data() {
        return {
            // options the student has chosen
            // CHANGE LATER FROM REQUEST

            availableOptions: [],
            availableOptionsPage: 1,

            chosenOptions: [],
            chosenOptionsPage: 1,

            fetching: true,
            // student data
            availableOptionsSearch: "",
            chosenOptionsSearch: "",
            displaySubjectInfo: false,
            displaySubjectDetails: {},
            // messages
            errorMessage: "",
            successMessage: "",

            changesMade: false,
        }
    },
    beforeMount() {
        this.getData()
    },
    computed: {
        getFilteredAOptions() {
            // filter available options through the search
            if (this.fetching) {
                return []
            } else {
                let startingPage = (this.availableOptionsPage - 1) * AVAILABLE_OPTIONS_PER_PAGE
                return [...[...this.availableOptions].filter(
                    option => option.title.toLowerCase().includes(this.availableOptionsSearch.toLowerCase())
                )].slice(startingPage, startingPage + AVAILABLE_OPTIONS_PER_PAGE)
            }
        },
        getFOMPagination() {
            return Math.floor(this.chosenOptions.length / CHOSEN_OPTIONS_PER_PAGE)

        },
        getFilteredCOptions() {
            // get chosen options through the search
            if (this.fetching) {
                return []
            } else {

                let startingPage = (this.chosenOptionsPage - 1) * CHOSEN_OPTIONS_PER_PAGE
                return [...[...this.chosenOptions].filter(
                    option => option.title.toLowerCase().includes(this.chosenOptionsSearch.toLowerCase())
                )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
            }
        },
        getFAMPagination() {
            return Math.floor(this.availableOptions.length / AVAILABLE_OPTIONS_PER_PAGE)

        },
    },
    methods: {
        getData() {
            axiosInstance.get(
                `api-rooms/rooms/${this.$route.params.room_id}/available-options`
            ).then(
                response => {
                    this.availableOptions = response.data.all
                    this.availableOptionsCount = response.data.all.length

                    this.chosenOptions = response.data.room
                    this.chosenOptionsCount = response.data.room.length
                    this.fetching = false
                }

            )
        },
        appendToChosenOptions({
            added
        }) {

            this.chosenOptions = [added.element, ...this.chosenOptions]
        },
        changeAvailableOptions({
            removed
        }) {
            let copied = [...this.availableOptions]
            copied.splice(removed.oldIndex, 1)
            this.availableOptions = copied
        },
        // dragging validation
        checkMoveOption(event) {
            this.errorMessage = ""
            this.changesMade = true
            if (event.to.id == "chosenOptions") {
                for (let i = 0; i < this.chosenOptions.length; i++) {
                    if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid) {
                        this.errorMessage = "This subject has already been chosen"
                        return false
                    }
                }
            }
        },
        removeChosenOption(element) {
            this.changesMade = true
            this.errorMessage = ""
            this.chosenOptions = [...this.chosenOptions].filter(e => e.id != element.id)
            this.availableOptions = [...this.availableOptions, element]
        },
        // subject info
        loadSubjectInfo(subject) {
            this.displaySubjectInfo = true
            this.displaySubjectDetails = subject
        },
        closeSubjectInfo() {
            this.displaySubjectInfo = false
        },
        // moving and removing all subjects
        useAllSubjects() {
            this.chosenOptions = [...this.chosenOptions, ...this.availableOptions]
            this.availableOptions = []
        },
        removeAllSubjects() {
            this.availableOptions = [...this.availableOptions, ...this.chosenOptions]
            this.chosenOptions = []
        },

        saveChoices() {
            this.fetching = true

            axiosInstance.put(`api-rooms/available-option-choices/${this.$route.params.opts_id}/batch_update/`, {
                "options": this.chosenOptions,
            }).then(response => {
                if (response.status == "200") {
                    this.errorMessage = ""
                    this.successMessage = "saved successfully"
                    this.changesMade = false
                    this.getData()

                } else if (response.status == "400") {
                    this.successMessage = ""
                    this.errorMessage = response.data.detail
                }

            })
        }

    }

});
</script>
