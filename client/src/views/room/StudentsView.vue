<template>
<q-page class="q-pa-none" padding>
    <div class="q-pa-md" style="width:100%">
        <q-card class="bg-grey-3 q-mt-md" style="min-height:78vh">
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
                <div class="col-2">
                    last name
                </div>
                <div class="col-1">
                    # options
                </div>
                <div class="col">
                    options
                </div>
                <div class="col-1">
                    actions
                </div>
            </div>
            <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                <div v-if="!fetching">
                    <q-scroll-area style="height:71vh" >
                        <q-card flat square v-for="student in students" :key="student.id">
                            <div class="row">
                                <div class="col-1">
                                    <q-btn color="grey" :label="student.uuid.slice(0,12)" size="sm" style="width:20vh" square>
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
                                    {{student.email}}
                                </div>
                                <div class="col-1">
                                    {{student.first_name}}
                                </div>
                                <div class="col-2">
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
                                    <q-btn flat dense class="bg-red q-ma-xs" color="white" icon="delete" />
                                </div>
                            </div>
                            <q-separator />
                        </q-card>
                    </q-scroll-area>
                </div>
            </transition>
            <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

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

export default defineComponent({
    name: "StudentsView",
    data() {
        return {
            students: [],
            fetching: false
        }
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
        }
    }
})
</script>
