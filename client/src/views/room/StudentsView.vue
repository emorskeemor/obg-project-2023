<template>
<q-page class="q-pa-none" padding>
    <div class="q-pa-md" style="width:100%">
        <q-card class="bg-grey-3 q-mt-md" style="min-height:77vh">
            <q-input filled v-model="search" label="Search chosen options" lazy-rules type="text">
                <template v-slot:prepend>
                    <q-icon name="search" />
                </template>
            </q-input>
            <div class="row justify-center items-center q-pa-md">
                <div class="col-1">
                    id
                </div>
                <div class="col-3">
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
                <div class="col-1">
                    actions
                </div>
            </div>
            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <div v-if="!fetching">
                    <q-card flat square v-for="student in getFilteredOptions" :key="student.id">
                        <div class="row justify-center items-center">
                            <div class="col-1">
                                <q-btn color="grey" :label="student.uuid.slice(0,12)" size="sm" style="width:20vh;height: 6vh;" square>
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
                            <div class="col-3">
                                <div class="row justify-center items-center">
                                    <q-input v-model="student.email" style="width:40vh" standout dense/>
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
                                </div>
                            </div>
                            <div class="col-1">
                                <div class="row justify-center items-center">
                                    <q-input v-model="student.max_choices" style="width:8vh" standout dense/>
                                </div>

                            </div>
                            <div class="col-1">
                                <div class="row">
                                    <q-btn flat dense class="bg-red q-ma-xs" color="white" icon="delete" />

                                </div>
                            </div>
                        </div>
                        <q-separator />
                    </q-card>
                </div>
            </transition>
            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />
            <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
                <q-pagination v-model="page" :max=studentPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />
                <q-btn label="save" color="green" @click="saveStudents"/>
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
        }
    },
    watch: {
        search() {
            this.page = 1
        }
    },
    computed: {
        studentPagination() {
            return Math.floor(this.students.length / CHOSEN_OPTIONS_PER_PAGE)

        },
        getFilteredOptions() {
            // get chosen options through the search
            if (this.fetching) {
                return []
            } else {

                let startingPage = (this.page - 1) * CHOSEN_OPTIONS_PER_PAGE
                return [...[...this.students].filter(
                    student => student.first_name.toLowerCase().includes(this.search.toLowerCase())
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
            axiosInstance.put(`api-students/students/${this.$route.params.room_id}/room-students/`, {
                students: this.students
            }).then(
                response => {
                    this.students = response.data
                    this.fetching = false

                }
            )
        }
    }
})
</script>
