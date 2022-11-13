<template>
    <q-page class="q-pa-xs no-scroll" padding >
        <q-card style="width:100vh;padding:5vh" class="absolute-center bg-grey-3">
          <div class="text-h1 main-font">
            Student access
          </div>
          <div class="text-h5 text-center q-pb-xl">Enter your school credentials</div> 

        <div class="q-gutter-md">
          <!-- email input -->
          <div class="fit row wrap justify-center items-start">
          <q-input
              filled v-model="email" label="email *" hint="email"
              lazy-rules
              type="text"
              :error="error"
              :rules="[val => !!val || 'field is required']"
              style="width:60vh"

          >
          <template v-slot:prepend>
              <q-icon name="mail"/>
          </template>
          </q-input>
        </div>

        <!-- first name input -->
        <div class="fit row wrap justify-center items-start">

          <q-input
              filled v-model="firstName" label="first name *" hint="first name"
              lazy-rules
              type="text"
              :error="error"
              :rules="[val => !!val || 'field is required']"
              style="width:60vh"

          >
          <template v-slot:prepend>
              <q-icon name="person"/>
          </template>
          </q-input>
        </div>
        <!-- last name input -->
        <div class="fit row wrap justify-center items-start">

          <q-input
              filled v-model="lastName" label="last name *" hint="last name"
              lazy-rules
              type="text"
              :error="error"
              :error-message="errorMessage"
              :rules="[val => !!val || 'field is required']"
              style="width:60vh"

          >
          <template v-slot:prepend>
              <q-icon name="person"/>
          </template>
          </q-input>

        </div>
        <!-- attempt to enter button -->
        <q-btn class="bg-green-13 text-white" push size="20px" @click="attemptEnter" label="Continue" icon-right="login"/>

      </div>

    </q-card> 
    <BannerComponent v-if="serverError" :message="serverErrorMessage" @dismiss="dismissAllErrors" colour="red"/>
      
    </q-page>
</template>

<script lang="ts">
import { axiosInstance } from '@/api/axios';
import BannerComponent from '@/components/misc/BannerComponent.vue';
import { defineComponent } from 'vue';


    
export default defineComponent({
  name: 'StudentCrendentials',
  components: {
    BannerComponent
  },
  data(){
    return {
        email: "",
        firstName: "",
        lastName: "",
        // error handling
        errorMessage:"",
        error: false ,

        serverError: false,
        serverErrorMessage: ""

    }
  },
  methods:{
    attemptEnter(){
      this.error = false
      this.errorMessage = ""
      // do some validation

      // NOTE THIS VALIDATION IS FOR TESTING AND SHOULD BE REWORKED FOR MORE 
      // ACCURATE ERROR MESSAGES

      if (this.email.length != 0 && this.firstName.length != 0 && this.lastName.length != 0 ){
        axiosInstance.post(`api-rooms/rooms/join/`, {
        // room details
        code:this.$route.params.code,
        domain:this.$route.params.domain,
        // student details
        first_name:this.firstName,
        last_name:this.lastName,
        email:this.email

      }).then(
        response=>{          
      
          if (response.status === 200) {
            // joining was successful
            const studentID = response.data.student_uuid
            const params = this.$route.params
            this.$router.push({name:"student-choice", params:{
              domain:params.domain,
              code:params.code,
              id:studentID
            }})
          }
          else {
            // raise error message from the server
            this.serverError = true
            this.serverErrorMessage = response.data.detail
            }
          }
        )

      } else {
        // handle the error
          this.error = true
          if (this.email.length <= 0) {
            this.errorMessage = "an email is required"
          } else if (this.lastName.length <= 0) {
            this.errorMessage = "a last name is required"
          } else if (this.firstName.length <= 0) {
            this.errorMessage = "a first name is required"
          }
        }
    },
    dismissAllErrors() {
      this.error = false
      this.errorMessage = ""
      this.serverError = false
      this.serverErrorMessage = ""
    }
  }
});
</script>
