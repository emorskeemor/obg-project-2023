<template>
    <q-page padding>
      <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
        Are you a...
      </h1>
      <div class="q-pa-md q-gutter-lg">
        <q-btn size="40px" push @click="$router.push(`/E401`)">student</q-btn>
        <q-btn size="40px" push>Teacher</q-btn>
        
      </div>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';
import { RouteLocationRaw } from 'vue-router';

export default defineComponent({
  name: 'HomeView',
  data(){
    return {
      loggedIn: isLoggedIn()
    }
  },
});
</script>
