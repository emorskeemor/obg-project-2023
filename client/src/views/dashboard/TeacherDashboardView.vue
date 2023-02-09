<template>
<q-page class="absolute-center" padding style="width:100%">

    <!-- current rooms  -->
    <div class="row q-gutter-xl">
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md shadow-15" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h3 main-font text-weight-medium q-ma-sm">Your Rooms</div>
                    <div class="row justify-center">
                        <div class="col-8">
                            <q-input filled v-model="search" label="Search" lazy-rules type="text">
                                <template v-slot:prepend>
                                    <q-icon name="search" />
                                </template>
                            </q-input>
                        </div>
                        <div class="col">

                            <q-btn label="create" icon="add_circle" class="bg-teal-3 text-white full-height" @click="displayCreatePopup=true" />
                        </div>
                    </div>

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
                            <q-input label="first name" class="full-width" v-model="userDetails.first_name" :rules="[val=>!!val || 'a first name is required']" />
                        </div>
                        <div class="row">
                            <q-input label="last name" class="full-width" v-model="userDetails.last_name" :rules="[val=>!!val || 'a last name is required']" />
                        </div>
                        <div class="row">
                            <q-input label="email" class="full-width" v-model="userDetails.email" :rules="[val=>!!val || 'an email is required']" />
                        </div>

                    </div>
                </q-card-section>
                <q-card-section class="bg-grey-4 absolute-bottom">
                    <q-btn label="save" icon="save" class="bg-teal-3 text-white" @click="saveUserDetails" size="md" />

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
                    <BlocksList :blocks=getFilteredBlocks @delete="deleteBlock" @info="blockInfo" />
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
                <q-input v-model="newRoomName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="room name" hint="name of the new room" :rules="[val=>!!val || 'a room name is required']">
                    <template v-slot:prepend>
                        <q-icon name="home" />
                    </template>
                </q-input>
                <q-input v-model="newSettingsName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="settings name" hint="name of the settings you'll will be using" :rules="[val=>!!val || 'a room name is required']">
                    <template v-slot:prepend>
                        <q-icon name="settings" />
                    </template>
                </q-input>
                <q-input v-model="newDomainName" autofocus @keyup.enter="displayCreatePopup=false" outlined label="domain name" hint="name of school domain" :rules="[val=>!!val || 'a room name is required']">
                    <template v-slot:prepend>
                        <q-icon name="domain" />
                    </template></q-input>
            </q-card-section>

            <q-card-actions align="right" class="text-primary">
                <q-btn label="Cancel" v-close-popup color="red" />
                <q-btn label="Create" color="green" @click="createRoom" />
            </q-card-actions>
        </q-card>
    </q-dialog>
    <q-dialog v-model="showBlockInfo">
        <ResultsPopup :data="currentBlock" />
    </q-dialog>
    
</q-page>
<BannerComponent colour="green" :message="successMessage" @dismiss="this.successMessage=''" v-if="successMessage.length !== 0" />
<BannerComponent colour="red" :message="errorMessage" @dismiss="this.errorMessage=''" v-if="errorMessage.length !== 0" />
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
import ResultsPopup from '@/components/misc/ResultsPopup.vue';
import BlocksList from '@/components/misc/BlocksList.vue';
import BannerComponent from '@/components/misc/BannerComponent.vue';

const CHOSEN_OPTIONS_PER_PAGE = 2

export default defineComponent({
    name: 'TeacherDashboardView',
    components: {
        RoomItem,
        ResultsPopup,
        BlocksList,
        BannerComponent
    },
    data() {
        return {
            loggedIn: false,
            // current rooms
            currentRooms: [],
            currentBlocks: [],
            currentBlock: {},

            search: "",
            blockSearch: "",
            page: 1,
            blockPage: 1,

            showBlockInfo: false,
            // data used to create 
            // new room
            displayCreatePopup: false,
            newRoomName: "",
            newSettingsName: "",
            newDomainName: "",
            userDetails: {},

            errorMessage: "",
            successMessage: "",
            fetching: false,

        }
    },
    computed: {
        roomPagination() {
            return Math.floor(this.currentRooms.length - 1 / CHOSEN_OPTIONS_PER_PAGE) + 1

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
            return Math.floor(this.currentBlocks.length - 1 / CHOSEN_OPTIONS_PER_PAGE) + 1

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
                () => {
                    this.fetchRooms()
                    this.successMessage = "Room deleted successfully"
                })
        },
        deleteBlock(block) {
            // delete a given room
            axiosInstance.delete(`api-generate/option-blocks/${block.id}`).then(
                () => {
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
            this.errorMessage = ""
            if (this.checkAllNotEmpty(
                    [
                        this.newDomainName, 
                        this.newSettingsName, 
                        this.newRoomName
                    ]
                ) === false) {
                this.errorMessage = "please fix any outstanding errors"
            } else {
                axiosInstance.post(`api-rooms/rooms/`, {
                    domain: this.newDomainName,
                    settings_title: this.newSettingsName,
                    title: this.newRoomName,
                }).then(() => {
                    this.fetchRooms()
                    this.displayCreatePopup = false
                    this.successMessage = "Room created successfully"
                })
            }
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
        saveUserDetails() {
            if (this.checkAllNotEmpty(
                    [
                        this.userDetails.first_name,
                        this.userDetails.last_name,
                        this.userDetails.email,
                    ]
                ) === false) {
                this.errorMessage = "please fix any outstanding errors"
            } else {
                axiosInstance.patch(`api-users/users/${this.$route.params.user_id}/`, {
                    email: this.userDetails.email,
                    first_name: this.userDetails.first_name,
                    last_name: this.userDetails.last_name,
                }).then(() => {
                    this.successMessage = "Details saved succesfully"
                }).catch(error => {
                    this.errorMessage = "Error while saving"
                })
            }
        },
        // UTILTIY METHODS
        checkAllNotEmpty(items) {
            for (let i = 0; i < items.length; i++) {
                if (items[i].length === 0) {
                    return false
                }
            }
            return true
        },
        emptyCheck(value) {
            return value.length == 0
        }

    }

});
</script>
