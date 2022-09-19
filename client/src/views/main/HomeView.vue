<template>
    <q-page padding>
      <!-- <div v-if="!loggedIn">
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
      </div> -->
      <!-- <div v-else>
        <TeacherDashboard/>
      </div> -->

      <div>
        <TeacherDashboard/>
      </div>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';
import TeacherDashboard from '@/components/auth/TeacherDashboard.vue'

export default defineComponent({
  name: 'HomeView',
  components:{
    TeacherDashboard
  },
  data(){
    return {
      loggedIn: isLoggedIn()
    }
  },
});
</script>
