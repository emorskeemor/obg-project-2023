
<template>
    <q-page class="q-pa-xl absolute-center" style="width:500px" padding >
      <h1 class="text-h2">Teacher login</h1>
      <q-form @submit="handleLogin()" @reset="handleReset()" class="q-gutter-md">
        <q-input
          filled
          v-model="email"
          label="Your email *"
          hint="email"
          lazy-rules
          type="email"
        >
        <template v-slot:prepend>
          <q-icon name="mail"/>
        </template>
        </q-input>

        <q-input
          filled
          v-model="password"
          label="Your password *"
          hint="password"
          lazy-rules
          type="password"
          autocomplete="on"
          >
        <template v-slot:prepend>
          <q-icon name="password"/>
        </template>
        </q-input>
        <div class="q-gutter-md">
          <q-btn class="bg-green-13 text-white" push size="20px" @click="handleLogin">
            Login
          </q-btn>
          <q-btn class="bg-red-13 text-white" push size="20px" @click="handleReset">
            Reset
          </q-btn>
        </div>
        <div v-if="errmsg !== ''">
          {{errmsg}}
        </div>
      </q-form>
    </q-page>

</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { login } from '@/api/auth'



export default defineComponent({
    name:"LoginView",
    data() {
        return {
            password:"",
            email:"",
            errmsg:''
        }
    },
    methods:{
        handleLogin(){
            console.log("logging in attempt");
            login({'email':this.email, 'password':this.password}).then(
              res=>{
                console.log("successful login");
                this.$router.push({"name":"home"})
              }
            ).catch(err=>{
              this.$data.errmsg = err.response.data.detail
            })

        },
      handleReset(){
        this.password = ""
        this.email = ""
        this.errmsg = ""
      }
    }
})
</script>