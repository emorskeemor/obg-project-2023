<template>
<q-page class="absolute-center" padding style="width:100%">

    <!-- current rooms  -->
    <div class="row q-gutter-xl">
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h3 main-font text-weight-medium q-ma-sm">Your Rooms</div>
                    <q-input filled v-model="search" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <q-scroll-area style="height:50vh">
                    <RoomItem v-for="room in getFilteredRooms" :key='room' :room='room' @onDelete="deleteRoom" @onEdit="editRoom" />

                </q-scroll-area>
                <q-card-section class="row justify-center bg-grey-4 absolute-bottom">
                    <q-pagination v-model="page" :max=roomPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />

                </q-card-section>
            </q-card>
        </div>
        <!-- middle column -->
        <div class="col">
            <q-card class="bg-grey-3 shadow-15" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">
                        Welcome to your dashboard {{ userDetails.first_name }}
                    </div>
                </q-card-section>
                <q-card-section>
                    <div class="main-font text-body2">
                        Here you can view and create rooms which students can access. You can then configure settings
                        get to generating option blocks
                    </div>
                    <div class="q-gutter-md">
                        <div class="row">
                            <q-input label="first name" class="full-width" v-model="userDetails.first_name" />
                        </div>
                        <div class="row">
                            <q-input label="last name" class="full-width" v-model="userDetails.last_name" />
                        </div>
                        <div class="row">
                            <q-input label="email" class="full-width" v-model="userDetails.email" />
                        </div>
                    </div>
                </q-card-section>
                <q-card-section class="bg-grey-4 absolute-bottom">
                    <q-btn label="create new room" icon="add_circle" class="bg-teal-3 text-white" @click="displayCreatePopup=true" />

                </q-card-section>
            </q-card>
        </div>
        <!-- generated blocks -->
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h3 main-font text-weight-medium q-ma-sm">Generated blocks</div>
                    <q-input filled v-model="blockSearch" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <q-card-section>
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
                <q-card-section class="row justify-center bg-grey-4 absolute-bottom">
                    <q-pagination v-model="blockPage" :max=blocksPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />

                </q-card-section>
            </q-card>
        </div>
    </div>
    <q-dialog v-model="displayCreatePopup">
        <q-card style="min-width: 60vh" class="q-pa-md">
            <q-card-section>
                <div class="text-h4 text-center">Create a new room</div>
            </q-card-section>

            <q-card-section class="q-gutter-md">
                <q-input v-model="newRoomName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="room name" hint="name of the new room">
                    <template v-slot:prepend>
                        <q-icon name="home" />
                    </template>
                </q-input>
                <q-input v-model="newSettingsName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="settings name" hint="name of the settings you'll will be using">
                    <template v-slot:prepend>
                        <q-icon name="settings" />
                    </template>
                </q-input>
                <q-input v-model="newDomainName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="domain name" hint="name of school domain">
                    <template v-slot:prepend>
                        <q-icon name="domain" />
                    </template></q-input>
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn label="Cancel" v-close-popup color="red" />
                <q-btn label="Create" v-close-popup color="green" @click="createRoom" />
            </q-card-actions>
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
</q-page>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';
import {
    isLoggedIn
} from 'axios-jwt';
import {
    axiosInstance
} from '@/api/axios';
import RoomItem from '@/components/dashboard/RoomItem.vue';

const CHOSEN_OPTIONS_PER_PAGE = 2

export default defineComponent({
    name: 'TeacherDashboardView',
    components: {
        RoomItem,
    },
    data() {
        return {
            loggedIn: false,
            currentRooms: [],
            currentBlocks: [],
            fetching: false,
            search: "",
            blockSearch: "",
            displayCreatePopup: false,
            showBlockInfo: false,
            currentBlock: {},
            newRoomName: "",
            newSettingsName: "",
            newDomainName: "",
            userDetails: {},

            page: 1,
            blockPage: 1,

        }
    },
    computed: {
        roomPagination() {
            return Math.floor(this.currentRooms.length-1 / CHOSEN_OPTIONS_PER_PAGE)

        },
        getFilteredRooms() {
            // get chosen options through the search
            if (this.fetching) {
                return []
            } else {

                let startingPage = (this.page - 1) * CHOSEN_OPTIONS_PER_PAGE
                return [...[...this.currentRooms].filter(
                    room => room.domain.toLowerCase().includes(this.search.toLowerCase())
                )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
            }
        },
        blocksPagination() {
            return Math.floor(this.currentBlocks.length-1 / CHOSEN_OPTIONS_PER_PAGE)

        },
        getFilteredBlocks() {
            // get chosen options through the search
            if (this.fetching) {
                return []
            } else {

                let startingPage = (this.blockPage - 1) * CHOSEN_OPTIONS_PER_PAGE
                return [...[...this.currentBlocks].filter(
                    block => block.title.toLowerCase().includes(this.blockSearch.toLowerCase())
                )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)
            }
        },
    },
    beforeMount() {
        // get the users room if any
        this.fetching = true
        this.fetchRooms()
        this.loggedIn = isLoggedIn()
    },
    methods: {
        deleteRoom(room) {
            // delete a given room
            axiosInstance.delete(`api-rooms/rooms/${room.pk}`).then(
                response => {
                    this.fetchRooms()
                })
        },
        deleteBlock(block) {
            // delete a given room
            axiosInstance.delete(`api-generate/option-blocks/${block.id}`).then(
                response => {
                    this.fetchRooms()
                })
        },
        blockInfo(block) {
            this.currentBlock = block
            this.showBlockInfo = true
        },
        fetchRooms() {
            // fetch the rooms created by the user and update the array of rooms
            axiosInstance.get(`api-users/users/${this.$route.params.user_id}/rooms`).then(
                (response) => {
                    this.currentRooms = response.data.rooms
                    this.userDetails = response.data.user
                    this.currentBlocks = response.data.blocks
                    this.fetching = false

                })
        },
        createRoom() {
            axiosInstance.post(`api-rooms/rooms/`, {
                domain: this.newDomainName,
                settings_title: this.newSettingsName,
                title: this.newRoomName,
            }).then(response => {
                this.fetchRooms()
            })
        },
        editRoom(room) {
            this.$router.push({
                "name": "room-edit",
                params: {
                    user_id: this.$route.params.user_id,
                    room_id: room.pk,
                }
            })
        },

    }

});
</script>
