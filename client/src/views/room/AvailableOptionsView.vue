<template>
<q-page class="q-pa-xs no-scroll" padding>
    <div class="row q-gutter-xl q-pa-md">

        <!-- available options that the student can choose from -->
        <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 text-black main-font" style="padding-bottom:1vh">Choices</div>
                    <!-- search bar -->
                    <q-input filled v-model="availableOptionsSearch" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <!-- available options draggable zone -->
                <draggable v-if="!fetching" class="list-group" :list="getFilteredAOptions" :group="{name:'availableOptions', pull:'clone', put:false}" :clone="cloneOption" itemKey="title" :move="moveOption" id="availableOptions">
                    <!-- iterate over all available options in pagination -->
                    <template #item="{element}">
                        <AvailableOptionItem :element="element" @showInfo="loadSubjectInfo" />
                    </template>
                </draggable>

                <!-- display a message to display if no searched pages are found -->
                <div v-if="getFilteredAOptions.length <= 0 && !fetching">
                    <q-card class="bg-grey-5 rounded-borders" style="padding:5vh;margin:3vh">
                        <div class="text-h4 text-black main-font">Whoopsie!</div>
                        <div class="text-h6">We could not find the subject you are looking for.</div>
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
                <div class="text-h4">Available options</div>
                <q-separator color="black" spaced />

                <div class="text-body1"><b>Drag</b> the subjects you would like to take into the chosen subjects section to the <b>right</b></div>

                <div class="text-body1 q-mt-md">These subjects on the right will be available to the students and will be used during generation</div>
                <div class="text-body1 q-mt-md"><div class="text-weight-bold">'Use all'</div> will make all the possible option choices available to the students</div>
                <div class="text-body1 q-mt-md"><div class="text-weight-bold">'Remove all'</div> will make remove all the possible option choices available to the students</div>

                <div class="absolute-bottom justify-center bg-grey-4" style="padding:10px">
                    <q-btn-group>
                        <q-btn class="bg-teal-4 text-white" size="md" label="use all" @click="useAllSubjects" />
                        <q-btn class="bg-teal-3 text-white" size="xl" label="Save" />
                        <q-btn class="bg-red text-white" size="md" label="remove all" @click="removeAllSubjects" />
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
                    <div class="text-h4 text-black main-font q-pa-md">Chosen options</div>
                    <q-input filled v-model="chosenOptionsSearch" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <draggable class="list-group" :list="getFilteredCOptions" :group="{name:'chosenOptions', pull:true, put:true}" @change="appendToChosenOptions" itemKey="name" id="chosenOptions">
                    <template #item="{element}">
                        <OptionItem :element="element" @showInfo="loadSubjectInfo" @removeOption="removeChosenOption" v-if="!fetching" itemStyle="width:55vh;margin:1vh;max-height:15vh;" />
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
import OptionItem from '@/components/options/OptionItem.vue';
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
        OptionItem,
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
        // we need to fetch some information before the data is rendered
        this.fetching = true
        // get the student
        axiosInstance.get(
            `api-rooms/rooms/${this.$route.params.room_id}/available-options`
        ).then(
            response => {
                console.log(response);
                this.availableOptions = response.data.all
                this.availableOptionsCount = response.data.all.length

                this.chosenOptions = response.data.room
                this.chosenOptionsCount = response.data.room.length
                this.fetching = false
            }

        )
    },
    computed: {
        getFilteredAOptions() {
            if (this.fetching) {
                return []
            } else {
                let startingPage = (this.availableOptionsPage - 1) * AVAILABLE_OPTIONS_PER_PAGE
                return [...[...this.availableOptions].filter(
                    option => option.title.toLowerCase().includes(this.availableOptionsSearch)
                )].slice(startingPage, startingPage + AVAILABLE_OPTIONS_PER_PAGE)
            }
        },
        getFOMPagination() {
            return Math.floor(this.chosenOptions.length / CHOSEN_OPTIONS_PER_PAGE)

        },
        getFilteredCOptions() {
            if (this.fetching) {
                return []
            } else {
                let startingPage = (this.chosenOptionsPage - 1) * CHOSEN_OPTIONS_PER_PAGE
                // console.log(startingPage, startingPage + OPTIONSPERPAGE);
                return [...[...this.chosenOptions].filter(
                    option => option.title.toLowerCase().includes(this.chosenOptionsSearch)
                )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
            }
        },
        getFAMPagination() {
            return Math.floor(this.availableOptions.length / AVAILABLE_OPTIONS_PER_PAGE)

        },
        filterBySearch(iterable, searchName) {
            return [...iterable].filter(option => option.contains(searchName))
        }
    },
    methods: {
        appendToChosenOptions({
            added
        }) {
            this.chosenOptions = [...this.chosenOptions, added.element]
        },
        moveOption(event) {
            // validate reseve options
            this.errorMessage = ""
            this.changesMade = true
            // validate chosen options
            if (event.to.id == "chosenOptions") {
                for (let i = 0; i < this.chosenOptions.length; i++) {
                    if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid) {
                        this.errorMessage = "This subject has already been chosen"
                        return false
                    }
                }
            }
            return true
        },
        cloneOption(option) {
            return option
        },
        removeChosenOption(index) {
            this.changesMade = true

            this.errorMessage = ""
            this.chosenOptions.splice(index, 1)
        },
        loadSubjectInfo(subject) {
            this.displaySubjectInfo = true
            this.displaySubjectDetails = subject
        },
        closeSubjectInfo() {
            this.displaySubjectInfo = false
        },
        useAllSubjects() {
            this.chosenOptions = [...this.availableOptions]
        },
        removeAllSubjects() {
            this.chosenOptions = []
        },

        saveChoices() {
            axiosInstance.put(`api-students/choices/${this.studentData.id}/update_student_options/`, {
                "main_options": this.chosenOptions,
                "code": this.$route.params.code,
                "domain": this.$route.params.domain,
                "reserve_options": this.reserveOptions,
            }).then(response => {
                if (response.status == "200") {
                    this.errorMessage = ""
                    this.successMessage = "saved successfully"
                    this.changesMade = false

                } else if (response.status == "400") {
                    this.successMessage = ""
                    this.errorMessage = response.data.detail
                }

            })
        }

    }

});
</script>
