<template>
    <q-page padding>
      <div v-if="!loggedIn">
        <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">
          Are you a...
        </h1>
        <div class="q-pa-md q-gutter-lg">
          <q-btn size="40px" push @click="$router.push(`/room/join`)" 
            class="bg-cyan-4 text-white"
            >
            student
          </q-btn>
          <q-btn size="40px" push @click="$router.push(`/auth/login`)" 
            class="bg-cyan-4 text-white"
            >
            Teacher
          </q-btn>
          
        </div>
      </div>
      
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';

export default defineComponent({
  name: 'HomeView',
  
  created(){
      this.$watch(
      () => this.$route.params,
      () => {        
        this.loggedIn = isLoggedIn()
      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
    )
    },
  data(){
    return {
      loggedIn: isLoggedIn()
    }
  },
});
</script>
