<template>
    <q-page class="q-pa-xs no-scroll" padding>
      <!-- header  -->
      <div class="bg-white text-black">
        <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        class="text-h1 text-center">
          Access a room
        </h1>
        <h1 class="text-h5 text-center q-pb-xl">Enter the details of the room bellow</h1>
      </div>
      <!-- domain name input -->
      <div class="q-gutter-md">
        <div class="fit row wrap justify-center items-start">

          <q-input
              filled
              v-model="domainName"
              label="Domain *"
              hint="domain"
              lazy-rules
              type="text"
              :error="error"
              :rules="[val => !!val || 'This field is required',]"
              style="width:60vh"
          >
          <template v-slot:prepend>
              <q-icon name="domain"/>
          </template>
          </q-input>
        </div>
        <!-- room code input -->
        <div class="fit row wrap justify-center items-start">
          <q-input
              filled
              v-model="roomCode"
              label="Room code *"
              hint="roomcode"
              lazy-rules
              type="text"
              :error="error"
              :error-message="errorMessage"
              :rules="[
              val => !!val || '* Required',
              val => val.length === 8 || 'A code is 8 characters long',]"
              style="width:60vh">
            <template v-slot:prepend>
                <q-icon name="home"/>
            </template>
          </q-input>
        </div>

      <!-- submit button to request access -->
        <q-btn class="bg-green-13 text-white" push size="20px" @click="handleAccess">
            Join
        </q-btn>

      </div>
      
    </q-page>
</template>

<script lang="ts">
import { axiosInstance } from '@/api/axios';
import { defineComponent } from 'vue';

export default defineComponent({
  name: 'RoomJoinView',
  data(){
    // define variables
    return {
        roomCode: "",
        domainName: "",
        // errors
        error:false,
        errorMessage:"",

        roomCodeLength: 8
    }
  },
  methods:{
    handleAccess(){
      // verify that the room does exist to allow access to the next stage
      this.error = false
      this.errorMessage = ""
      
      if (this.roomCode.length === this.roomCodeLength && this.domainName.length != 0){
        axiosInstance.get(`api-rooms/rooms/${this.roomCode}/?domain=${this.domainName}`).then(
          response=>{
            // push to room verification screen if the room was found
            if (response.status === 200) {
                this.$router.push({name:"room-verification", params:{
                  code:this.roomCode,
                  domain:this.domainName,
                }
              }
            )              
            } else {
              // display default error that was raised by the server            
              this.error = true
              this.errorMessage = "Room with given domain and room code not found"
            }
          }
        )
      } else {
        // validation
        this.error = true
        if (this.roomCode.length <= 0) {
          this.errorMessage = "room code is required"
        } else if (this.roomCode.length !== this.roomCodeLength) {
          this.errorMessage = "room code must be 8 characters"
        } else if (this.domainName.length <= 0) {
          this.errorMessage = "domain name is required"
        }


      }
    }
  }
});
</script>
