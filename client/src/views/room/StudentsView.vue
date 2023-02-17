<template>
<q-page class="q-pa-none" padding>
    <div class="q-pa-md" style="width:100%">
        <q-card class="bg-grey-3 q-mt-md" style="min-height:77vh">

            <div class="row">
                <div class="col-10">
                    <q-input filled v-model="search" label="Search for students" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </div>
                <div class="col">
                    <q-select v-model="searchBy" :options="searchOptions" label="search by ..." dense map-options class="q-pa-sm" />

                </div>
            </div>
            <div class="row justify-center items-center q-pa-md">
                <div class="col-1">
                    ID <q-chip dense icon="account_circle">{{ students.length }}</q-chip>

                </div>
                <div class="col-2">
                    email
                </div>
                <div class="col-1">
                    first name
                </div>
                <div class="col-1">
                    last name
                </div>
                <div class="col-1">
                    # options
                </div>
                <div class="col">
                    options
                </div>
                <div class="col-1">
                    max opts
                </div>
                <div class="col">
                    reserves
                </div>
                <div class="col-1">
                    max reserves
                </div>
                <div class="col-1">
                    actions
                </div>
                <div class="col-1">
                    ignore
                </div>
            </div>
            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <div v-if="!fetching">
                    <q-card flat square v-for="student in getFilteredOptions" :key="student.id">
                        <div class="row justify-center items-center">
                            <div class="col-1">
                                <q-btn color="grey" :label="student.uuid.slice(0,12)" size="sm" style="width:100%;height: 6vh;" square>
                                    <q-popup-proxy>
                                        <q-banner>
                                            <template v-slot:avatar>
                                                <q-icon name="account_circle" color="light-grey" />
                                            </template>
                                            <div class="row">
                                                student uuid: {{student.uuid}}
                                            </div>
                                            <div class="row">
                                                id : {{student.id }}
                                            </div>
                                        </q-banner>
                                    </q-popup-proxy>
                                </q-btn>
                            </div>
                            <div class="col-2">
                                <div class="row justify-center items-center">
                                    <q-input v-model="student.email" style="width:40vh" standout dense />
                                </div>
                            </div>
                            <div class="col-1">
                                {{student.first_name}}
                            </div>
                            <div class="col-1">
                                {{student.last_name}}
                            </div>
                            <div class="col-1">
                                {{student.options.length}}
                            </div>
                            <div class="col">
                                <div class="row justify-center items-center full-height">
                                    <div v-for="option in student.options" :key="option.uuid" class="col">
                                        <q-btn color="black" :label="option.subject_code" size="sm" square style="width:100%" class="bg-grey">
                                            <q-popup-proxy>
                                                <q-banner>
                                                    <template v-slot:avatar>
                                                        <q-icon name="account_circle" color="light-grey" />
                                                    </template>
                                                    <div class="row">
                                                        title: {{option.title}}
                                                    </div>
                                                    <div class="row">
                                                        uuid : {{option.uuid }}
                                                    </div>
                                                </q-banner>
                                            </q-popup-proxy>
                                        </q-btn>
                                    </div>
                                </div>
                            </div>
                            <div class="col-1">
                                <div class="row justify-center items-center">
                                    <q-input v-model="student.max_choices" style="width:8vh" standout dense />
                                </div>

                            </div>
                            <div class="col">
                                <div class="row">
                                    
                                    <div v-for="option in student.reserves" :key="option.uuid" class="col">
                                        <q-btn color="black" :label="option.subject_code" size="sm" square style="width:10vh" class="bg-grey">
                                            <q-popup-proxy>
                                                <q-banner>
                                                    <template v-slot:avatar>
                                                        <q-icon name="account_circle" color="light-grey" />
                                                    </template>
                                                    <div class="row">
                                                        title: {{option.title}}
                                                    </div>
                                                    <div class="row">
                                                        uuid : {{option.uuid }}
                                                    </div>
                                                </q-banner>
                                            </q-popup-proxy>
                                        </q-btn>
                                    </div>
                                    <div v-if="student.reserves.length <= 0">
                                        no reserves
                                    </div>
                                </div>
                            </div>
                            <div class="col-1">
                                <div class="row justify-center items-center">
                                    <q-input style="width:8vh" standout dense v-model="student.max_reserves"/>
                                </div>

                            </div>
                            <div class="col-1">
                                <q-btn flat dense class="bg-red q-ma-xs" color="white" icon="delete" @click="deleteStudent(student)"/>

                            </div>
                            <div class="col-1">
                                <q-checkbox v-model="student.ignore" />

                            </div>
                        </div>
                        <q-separator />
                    </q-card>
                </div>
            </transition>
            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />
            <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                <q-pagination v-model="page" :max=studentPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" 
                v-if="!fetching"/>
                <q-btn label="save" color="teal-4" @click="saveStudents" :disable="fetching"/>
            </div>
        </q-card>
    </div>
</q-page>
</template>

<script>
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';

const CHOSEN_OPTIONS_PER_PAGE = 9

export default defineComponent({
    name: "StudentsView",
    data() {
        return {
            students: [],
            page: 1,
            search: "",
            fetching: false,
            searchBy: {
                value: "first_name",
                label: "first name"
            },
            searchOptions: [{
                    value: "first_name",
                    label: "first name"
                },
                {
                    value: "last_name",
                    label: "last name"
                },
                {
                    value: "email",
                    label: "email"
                },
            ]
        }
    },
    watch: {
        search() {
            this.page = 1
        }
    },
    computed: {
        studentPagination() {
            return Math.floor(this.students.length / CHOSEN_OPTIONS_PER_PAGE) + 1

        },
        getFilteredOptions() {
            // get chosen options through the search
            if (this.fetching) {
                return []
            } else {

                let startingPage = (this.page - 1) * CHOSEN_OPTIONS_PER_PAGE
                return [...[...this.students].filter(
                    student => student[this.searchBy.value].toLowerCase().includes(this.search.toLowerCase())
                )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
            }
        },
    },
    beforeMount() {
        this.fetching = true
        this.getStudents()
    },
    methods: {
        getStudents() {
            axiosInstance.get(`api-students/students/${this.$route.params.room_id}/room-students`).then(
                response => {
                    this.students = response.data
                    this.fetching = false

                }
            )
        },
        saveStudents() {
            this.fetching = true
            axiosInstance.put(`api-students/students/${this.$route.params.room_id}/room-students/`, {
                students: this.students
            }).then(
                response => {
                    this.fetching = false

                }
            )
        },
        deleteStudent(student) {
            this.fetching = true
            axiosInstance.delete(`api-students/students/${student.id}/`).then(
                response => {
                    
                    this.fetching = false
                    this.students = this.students.filter(val=>val.id !== student.id)

                }
            )
        }
    }
})
</script>
