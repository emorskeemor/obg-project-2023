<template>
    <q-page class="absolute-center" padding >
        <div>
            <h1 class="text-h2" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
              Welcome to your dashboard
            </h1>
            
        </div>
        <div>

        </div>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn, getAccessToken } from 'axios-jwt';
import jwt_decode from 'jwt-decode'

export default defineComponent({
  name: 'TeacherDashboardView',
  data(){
    return {
      loggedIn: false
    }
  },
  created(){
    this.fetchUserData()
    this.loggedIn = isLoggedIn()
  },
  methods:{
    fetchUserData(){
      console.log("dashboard user", this.$route.params.user_id);
    }
  }
});
</script>