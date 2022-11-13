<template>
    <q-page class="absolute-center" padding style="width:100%">
        <!-- header -->
        <!-- <div class="q-pa-xs q-mb-md">
            <div class="text-h2 main-font">
              Welcome to your dashboard
            </div>
        </div> -->
        <!-- main body -->
        <!-- current rooms  -->
        <div class="row q-gutter-xl">
          <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
              <q-card-section  class="bg-grey-4">
                <div class="text-h4 main-font">Your Rooms</div>
                <q-input filled v-model="search" label="Search" lazy-rules type="text">
                  <template v-slot:prepend>
                      <q-icon name="search"/>
                  </template>
                </q-input>
              </q-card-section>
                <RoomItem v-for="room in currentRooms" :key='room' :room='room'/>
            </q-card>
          </div>
          <!-- middle column -->
          <div class="col">
            <q-card class="bg-grey-3" style="min-height:70vh">
              <q-card-section class="bg-grey-4" >
                <div class="text-h4 main-font">Welcome to your dashboard</div>
              </q-card-section>
              <q-card-section>
                <q-btn label="create new room" icon="add_circle" class="bg-teal-3 text-white"/>
              </q-card-section>
              <q-card-section class="bg-grey-4 absolute-bottom" >
                <div class="text-h4 main-font"></div>
              </q-card-section>
            </q-card>
          </div>
          <!-- generated blocks -->
          <div class="col-4">
            <q-card class="bg-grey-3 q-mt-md" style="min-height:75vh">
              <q-card-section  class="bg-grey-4">
                <div class="text-h4 main-font">Generated blocks</div>
              </q-card-section>
            </q-card>
          </div>
        </div>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';
import { axiosInstance } from '@/api/axios';
import RoomItem from '@/components/dashboard/RoomItem.vue';



export default defineComponent({
  name: 'TeacherDashboardView',
  components: {
    RoomItem
  },
  data(){
    return {
      loggedIn: false,
      currentRooms: [],
      fetching:false,
      search:"",
    }
  },
  beforeMount() {
    // get the users room if any
    this.fetching = true
    axiosInstance.get(`api-users/users/${this.$route.params.user_id}/rooms`).then(
      response=>{
        this.currentRooms = response.data
      }
    )
    this.loggedIn = isLoggedIn()
    this.fetching = false
  },
});
</script>