<template>
<q-page class="q-pa-xs no-scroll" padding>
    <div class="row q-gutter-xl q-pa-md">

        <!-- available options that the student can choose from -->
        <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 text-black main-font" style="padding-bottom:1vh">Available options</div>
                    <!-- search bar -->
                    <q-input filled v-model="search" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <!-- available options draggable zone -->
                <draggable v-if="!fetching" class="list-group" :list="getSearchedPages()" :group="{name:'availableOptions', pull:'clone', put:false}" :clone="cloneOption" itemKey="title" :move="moveOption" id="availableOptions">
                    <!-- iterate over all available options in pagination -->
                    <template #item="{element}">
                        <AvailableOptionItem :element="element" @showInfo="loadSubjectInfo" />
                    </template>
                </draggable>

                <!-- display a message to display if no searched pages are found -->
                <div v-if="getSearchedPages().length === 0 && !fetching">
                    <q-card class="bg-grey-5 rounded-borders" style="padding:5vh;margin:3vh">
                        <div class="text-h4 text-black main-font">Whoopsie!</div>
                        <div class="text-h6">We could not find the subject you are looking for.</div>
                    </q-card>
                </div>

                <!-- display a skeleton if the options have not yet loaded -->
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                <!-- pagination  -->
                <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                    <q-pagination v-model="availableOptionsPage" :max=maximumOptionPages :max-pages=5 direction-links push color="teal" active-design="push" active-color="red-5" :modelValue="availableOptionsPage" />
                </div>
            </q-card>

        </div>
        <!-- details about the option block choice -->

        <div class="col">
            <q-card class="bg-grey-3" style="padding:20px;min-height:75vh">
                <!-- details about how to choose the options -->
                <div class="text-h4 text-black main-font">Hello {{studentData.firstName}} {{studentData.lastName}}</div>
                <div class="text-body1">Drag the subjects you would like to take into the chosen subjects section to the right</div>

                <!-- display how may subjects the student can take -->
                <q-separator color="black" spaced />
                <div class="text-h6 text-black main-font text-weight-medium">You are able to take {{maximumAllowedOptions}} subjects</div>
                <div class="text-h6 text-black main-font text-weight-medium">and {{maximumReserveOptions}} reserve options</div>

                <q-separator color="black" spaced />
                <!-- reserve options -->
                <q-card-section class="block full-height">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div v-show="!fetching">

                            <draggable class="list-group" :list="reserveOptions" :group="{name:'reserveOptions', pull:true, put:true}" itemKey="name" id="reserveOptions">
                                <template #item="{element}">
                                    <OptionItem :element="element" @showInfo="loadSubjectInfo" @removeOption="removeReserveOption" v-if="!fetching" itemStyle="width:40vh;margin:1vh;max-height:15vh;" />
                                </template>
                            </draggable>
                        </div>
                    </transition>
                </q-card-section>
                <!-- save options and reserves -->
                <div class="absolute-bottom justify-center bg-grey-4" style="padding:10px">
                    <q-btn-group>
                        <q-btn class="bg-red-5 text-white" icon-right="check_circle" size="small" label="save" @click="saveChoices()" :disable="chosenOptions.length != maximumAllowedOptions || reserveOptions.length !== maximumReserveOptions" />
                        <q-btn class="bg-blue text-white" icon-right="help" size="small" label="help" />
                        <q-btn class="bg-light-blue text-white" icon-right="route" size="small" label="pathways" />

                    </q-btn-group>
                </div>
                <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />
            </q-card>
        </div>

        <!-- The chosen options the student has chosen -->
        <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 text-black main-font">Chosen options</div>
                </q-card-section>
                <draggable class="list-group" :list="chosenOptions" :group="{name:'chosenOptions', pull:true, put:true}" @change="changesMade=true" itemKey="name" id="chosenOptions">
                    <template #item="{element, index}">
                        <OptionItem :element="element" @showInfo="loadSubjectInfo" @removeOption="removeChosenOption" v-if="!fetching" itemStyle="width:55vh;margin:1vh;max-height:15vh;">
                            <q-badge color="red-12 row justify-center rounded-borders" floating rounded style="width:4vh;height:4vh">
                                <div class="text-h5 text-white">{{index+1}}</div>
                            </q-badge>
                        </OptionItem>
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

const optionsPerPage = 5

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
            chosenOptions: [],
            reserveOptions: [],
            // CHANGE LATER FROM REQUEST
            maximumReserveOptions: 2,
            maximumAllowedOptions: 0,

            availableOptions: [],
            availableOptionsPage: 1,
            availableOptionsCount: 0,
            maximumOptionPages: 0,

            fetching: true,
            // student data
            studentData: {
                firstName: "",
                lastName: "",
                uuid: ""
            },
            search: "",
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
        const params = this.$route.params
        this.fetching = true
        // get the student
        axiosInstance.get(
            `api-students/students/${params.id}`
        ).then(
            response => {
                if (response.status == "200") {
                    // student was found and we can get their current options
                    // if any and their allowed number of choices
                    const data = response.data
                    this.chosenOptions = [...data.options]
                    this.reserveOptions = [...data.reserves]
                    this.maximumAllowedOptions = data.max_choices
                    this.studentData.firstName = data.first_name
                    this.studentData.lastName = data.last_name
                    this.studentData.uuid = data.uuid
                    this.studentData.id = data.id
                    this.fetching = false

                } else if (response.status == "404") {
                    // a 404 means the student uuid in the url was invalid
                    // and we should redirect to a 404
                    this.$router.push({
                        name: "E404"
                    })
                }

            }
        )
        // get the available options for the student
        axiosInstance.get(
            `api-rooms/available-option-choices/room-choices/?domain=${params.domain}&code=${params.code}&page=${this.availableOptionsPage}`
        ).then(response => {
            this.availableOptions = response.data
            this.availableOptionsCount = this.availableOptions.length
            this.maximumOptionPages = Math.floor(this.availableOptionsCount / optionsPerPage) + 1

        })
    },
    beforeRouteLeave(to, from, next) {
        if (this.changesMade === true) {
            const answer = window.confirm('You have unsaved changes! Are you sure you want to leave this page?')
            if (answer) {
                next()
            } else {
                next(false)
            }
        } else {
            next()
        }
    },
    methods: {
        moveOption(event) {
            // validate reseve options
            this.errorMessage = ""
            this.changesMade = true
            if (event.to.id == "reserveOptions") {
                if (this.reserveOptions.length >= this.maximumReserveOptions) {
                    this.errorMessage = "Too many reserve options"
                    return false
                } else {
                    for (let i = 0; i < this.reserveOptions.length; i++) {
                        if (event.draggedContext.element.uuid === this.reserveOptions[i].uuid) {
                            this.errorMessage = "You have already chosen this subject as a reserve option"
                            return false
                        }
                    }
                    for (let i = 0; i < this.chosenOptions.length; i++) {
                        if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid) {
                            console.log("no thanks");
                            this.errorMessage = "This subject has already been used as a main option"
                            return false
                        }
                    }
                }
                // validate chosen options
            } else if (event.to.id == "chosenOptions") {
                if (this.chosenOptions.length >= this.maximumAllowedOptions) {
                    this.errorMessage = "Too many options"
                    return false
                } else {
                    for (let i = 0; i < this.reserveOptions.length; i++) {
                        if (event.draggedContext.element.uuid === this.reserveOptions[i].uuid) {
                            this.errorMessage = "You have already chosen this subject as a reserve option"
                            return false
                        }
                    }
                    for (let i = 0; i < this.chosenOptions.length; i++) {
                        if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid) {
                            this.errorMessage = "This subject has already been chosen"
                            return false
                        }
                    }
                }
            }
        },
        cloneOption(option) {
            return option
        },
        removeChosenOption(index) {
            this.changesMade = true

            this.errorMessage = ""
            this.chosenOptions.splice(index, 1)
        },
        removeReserveOption(index) {
            this.changesMade = true

            this.errorMessage = ""
            this.reserveOptions.splice(index, 1)
        },
        // searching and pagination
        searchFilter(option) {
            return (option.title.toLowerCase().includes(this.search))
        },
        getSearchedPages() {
            if (this.fetching) {
                return []
            }
            if (this.search === "") {
                return this.calculatePagination(this.availableOptions)
            } else {
                return this.calculatePagination(
                    this.availableOptions.filter(this.searchFilter)
                );
            }
        },
        calculatePagination(options) {
            let startingPage = (this.availableOptionsPage - 1) * optionsPerPage

            this.availableOptionsCount = options.length
            this.maximumOptionPages = Math.floor(this.availableOptionsCount / optionsPerPage)

            return options.slice(
                startingPage,
                startingPage + optionsPerPage
            )

        },
        loadSubjectInfo(subject) {
            this.displaySubjectInfo = true
            this.displaySubjectDetails = subject
        },
        closeSubjectInfo() {
            this.displaySubjectInfo = false
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
