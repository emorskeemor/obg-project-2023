<template>
    <q-page class="q-pa-xl absolute-center" padding >
      <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        class="text-h2" >
        Enter your details
      </h1>
      <div style="width:500px" >
        <q-input
            filled v-model="email" label="email *" hint="email"
            lazy-rules
            type="text"
            :error="error"
            :rules="[val => !!val || 'field is required']"
        >
        <template v-slot:prepend>
            <q-icon name="mail"/>
        </template>
        </q-input>
        <q-input
            filled v-model="firstName" label="first name *" hint="first name"
            lazy-rules
            type="text"
            :error="error"
            :rules="[val => !!val || 'field is required']"
        >
        <template v-slot:prepend>
            <q-icon name="person"/>
        </template>
        </q-input>
        <q-input
            filled v-model="lastName" label="last name *" hint="last name"
            lazy-rules
            type="text"
            :error="error"
            :error-message="errorMessage"
            :rules="[val => !!val || 'field is required']"
        >
        <template v-slot:prepend>
            <q-icon name="person"/>
        </template>
        </q-input>
       
        <q-btn class="bg-green-13 text-white" push size="20px" @click="attemptEnter">
            Continue
        </q-btn>

      </div>
      
    </q-page>
</template>

<script lang="ts">
    import { axiosInstance } from '@/api/axios';
    import { defineComponent } from 'vue';
    
export default defineComponent({
  name: 'StudentCrendentials',
  data(){
    return {
        email: "",
        firstName: "",
        lastName: "",
        // error handling
        errorMessage:"",
        error: false
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
        axiosInstance.post(`-rooms/rooms/join/`, {
        code:this.$route.params.code,
        domain:this.$route.params.domain,
        first_name:this.firstName,
        last_name:this.lastName,
        email:this.email
      }).then(
        res=>{          
          console.log(res);
          
          if (res.status === 200) {
            const studet_id = res.data.student_uuid
            const params = this.$route.params
            this.$router.push({name:"student-choice", params:{
              domain:params.domain,
              code:params.code,
              id:studet_id
            }})
            
          }
          else {
            this.error = true
            this.errorMessage = res.data.detail
          }
          
          
        }
        )

      }else {
            this.error = true
            this.errorMessage = "please fill in all inputs"
          }
    }
  }
});
</script>
