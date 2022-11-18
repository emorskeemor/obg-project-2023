<template>
    <q-layout view="lHh Lpr lFf" >
      <!-- navigation bar content -->
      <q-header elevated >
        <q-toolbar class="bg-teal-4 glossy" style="min-height:8vh">
          <q-toolbar-title >
            <div class="absolute-center cursor-pointer q-hoverable">
              <q-avatar size="60px" @click="returnHome" square>
                <img :src="require(`./assets/logo.png`)"/>
              </q-avatar>
              EDGBARROW
            </div>
          </q-toolbar-title>
          
          <!-- logout button -->
          <div v-if="loggedIn">
            <q-btn @click="handleLogout" class="bg-black">Logout</q-btn>
          </div>
        </q-toolbar>

      </q-header>

      <!-- main body for router view-->
      <q-page-container>
        <router-view />
        
      </q-page-container>

      <!-- ajax loading bar when sending requests -->
      <q-ajax-bar
      ref="bar"
      position="bottom"
      color="green-8"
      size="10px"
      />

      <!-- footer  -->
      <q-footer reveal elevated>
        <q-toolbar class="bg-teal-4">
          <q-btn class="bg-black" @click="$router.back()">Back</q-btn>
        </q-toolbar>
      </q-footer>
    </q-layout>

</template>

<script lang="ts">
  import { defineComponent } from 'vue';
  import { getAccessToken, isLoggedIn } from 'axios-jwt';
  import { logout } from './api/auth';
  import { DecodedTokenObject } from './api/interfaces';
  import jwtDecode from 'jwt-decode';
    
  
  export default defineComponent({
    name: 'App',
    created(){
      this.$watch(
      () => this.$route.params,
      () => {
        this.loggedIn = isLoggedIn()
      },
      { immediate: true }
    )
    },
    data(){
      return {
        loggedIn: false
      }
    },
    methods:{
      handleLogout(){
        // logout the user by removing the access and refresh tokens from local
        // storage and then change the flag, once done redirect back to the home page
        logout()
        this.loggedIn = false
        this.$router.push({name:"home", force:true})
      },
      returnHome(){
        // check that the user is still logged in. We do this by gettings the access token if
        // it is still present. If not, we know the user is no longer logged in
        const accessToken = getAccessToken()
        if (accessToken){
          logout()
        }
        else {
          this.$router.push({name:"home"})

        }
      }
    }
  });
  </script>
  

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

.main-font {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
</style>
