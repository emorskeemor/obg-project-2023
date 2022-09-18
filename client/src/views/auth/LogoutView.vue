<template>
    <q-layout view="lHr lpR lFr" class="shadow-2 rounded-borders">
        <q-page-container class="q-pa-xl absolute-center" style="width:500px" >
            <h1>Are you ready to logout?</h1>
            <q-btn @click="handleLogout()">Logout</q-btn>
        </q-page-container>

  </q-layout>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { logout } from '@/api/auth'



export default defineComponent({
    name:"LogoutView",
    methods:{
        handleLogout() {
            logout()
            console.log("successful logout");
            this.$router.push({"name":"home"})
        }
    }
})
</script>