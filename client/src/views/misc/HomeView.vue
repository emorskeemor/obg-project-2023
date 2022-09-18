<template>
  <div class="home">
    <router-link to="/auth/login" v-if="!loggedIn">Login</router-link>
    <router-link to="/auth/logout" v-if="loggedIn">Logout</router-link>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';

export default defineComponent({
  name: 'HomeView',
  data(){
    return {
      loggedIn: isLoggedIn()
    }
  },
});
</script>
