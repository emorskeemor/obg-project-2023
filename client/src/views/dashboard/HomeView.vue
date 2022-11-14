<template>
    <q-page padding>
      <div v-if="!loggedIn">
        <q-card style="width:100vh" class="absolute-center bg-grey-3">
          <q-card-section>
            <div class="main-font text-h1 text-weight-medium">
            Are you a...
            </div>
          </q-card-section>
          <div class="q-pa-md q-gutter-lg row justify-center">
              <div class="col-4">
                <q-btn size="40px" push @click="$router.push(`/room/join`)" icon="face"
                class="bg-cyan-4 text-white"
                >
                student
              </q-btn>
              </div>
              <div class="col-1">
                <div class="main-font text-h3 text-weight-medium">
                OR
                </div>
              </div>
              <div class="col-4">
                <q-btn size="40px" push @click="$router.push(`/auth/login`)" 
                icon="badge"
                class="bg-cyan-4 text-white"
                >
                Teacher
              </q-btn>
              </div>
            
          </div>

        </q-card>
      </div>
      
    </q-page>
</template>

<script lang="js">
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
