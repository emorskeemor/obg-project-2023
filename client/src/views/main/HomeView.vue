<template>
    <q-page padding>
      <div v-if="!loggedIn">
        <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
        Are you a...
      </h1>
      <div class="q-pa-md q-gutter-lg">
        <q-btn size="40px" push @click="$router.push(`/room/join`)">student</q-btn>
        <q-btn size="40px" push @click="$router.push(`/auth/login`)">Teacher</q-btn>
        
      </div>
      </div>
    </q-page>
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
