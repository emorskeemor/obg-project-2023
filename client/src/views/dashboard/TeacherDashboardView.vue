<template>
<q-page class="absolute-center" padding style="width:100%">

    <!-- current rooms  -->
    <div class="row q-gutter-xl">
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">Your Rooms</div>
                    <q-input filled v-model="search" label="Search" lazy-rules type="text">
                        <template v-slot:prepend>
                            <q-icon name="search" />
                        </template>
                    </q-input>
                </q-card-section>
                <RoomItem v-for="room in currentRooms" :key='room' :room='room' @onDelete="deleteRoom" @onEdit="editRoom" />
            </q-card>
        </div>
        <!-- middle column -->
        <div class="col">
            <q-card class="bg-grey-3" style="min-height:70vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">Welcome to your dashboard</div>
                </q-card-section>
                <q-card-section>
                    <q-btn label="create new room" icon="add_circle" class="bg-teal-3 text-white" @click="displayCreatePopup=true" />
                </q-card-section>
                <q-card-section class="bg-grey-4 absolute-bottom">
                    <div class="text-h4 main-font"></div>
                </q-card-section>
            </q-card>
        </div>
        <!-- generated blocks -->
        <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
                <q-card-section class="bg-grey-4">
                    <div class="text-h4 main-font">Generated blocks</div>
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

export default defineComponent({
    name: 'TeacherDashboardView',
    components: {
        RoomItem
    },
    data() {
        return {
            loggedIn: false,
            currentRooms: [],
            fetching: false,
            search: "",
            displayCreatePopup: false,
            newRoomName: "",
            newSettingsName: "",
            newDomainName: "",

        }
    },
    beforeMount() {
        // get the users room if any
        this.fetching = true
        this.fetchRooms()
        this.loggedIn = isLoggedIn()
        this.fetching = false
    },
    methods: {
        deleteRoom(room) {
            // delete a given room
            axiosInstance.delete(`api-rooms/rooms/${room.id}`).then(
                response => {
                    this.fetchRooms()
                })
        },
        fetchRooms() {
            // fetch the rooms created by the user and update the array of rooms
            axiosInstance.get(`api-users/users/${this.$route.params.user_id}/rooms`).then(
                (response) => {
                    this.currentRooms = response.data
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
                    domain: room.domain,
                }
            })
        }
    }

});
</script>
