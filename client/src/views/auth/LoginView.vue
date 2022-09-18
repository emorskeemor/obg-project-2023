
<template>
  <q-layout view="lHr lpR lFr" class="shadow-2 rounded-borders">
    <q-page-container class="q-pa-xl absolute-center" style="width:500px" >
        <q-form @submit="handleLogin()" @reset="handleReset()" class="q-gutter-md">
      <q-input
        filled
        v-model="username"
        label="username *"
        hint="Name and surname"
        lazy-rules
      />
      <q-input
        filled
        v-model="password"
        label="Your password *"
        hint="password"
        lazy-rules
        type="password"
        autocomplete="on"
      />
      <q-input
        filled
        v-model="email"
        label="Your email *"
        hint="email"
        lazy-rules
        type="email"
      />
      <div>
        <!-- <q-btn label="Submit" type="submit" color="primary"/>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" /> -->
        <button type="submit">submit</button>
        <button type="reset">reset</button>
      </div>
      <div v-if="errmsg !== ''">
        {{errmsg}}
      </div>
    </q-form>
    </q-page-container>

  </q-layout>
</template>

<script>
import { defineComponent } from 'vue';

import { login } from '@/api/auth'



export default defineComponent({
    name:"LoginView",
    data() {
        return {
            username:"",
            password:"",
            email:"",
            errmsg:''
        }
    },
    methods:{
        handleLogin(){
            console.log("logging in attempt");
            login({'email':this.email, 'password':this.password, 'username':this.username}).then(
              res=>{
                console.log("successful login");
                this.$router.push({"name":"home"})
              }
            ).catch(err=>{
              this.$data.errmsg = err.response.data.detail
            })

        },
      handleReset(){
        this.username = ""
        this.password = ""
        this.email = ""
        this.errmsg = ""
      }
    }
})
</script>