<template>
    <q-page  class="q-pa-xl absolute-center" padding >
        <div>
            <h1 class="text-h2" style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif">Hello {{user}}</h1>
        </div>
        <div>

        </div>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { isLoggedIn } from 'axios-jwt';

export default defineComponent({
  name: 'TeacherDashboard',
  data(){
    return {
      loggedIn: isLoggedIn(),
      user:"Mr.something"
    }
  },
});
</script>