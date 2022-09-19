<template>
    <q-layout view="lHh Lpr lFf" >
      <!-- header content -->
      <q-header elevated >
        <q-toolbar class="bg-teal-4 glossy" style="min-height:10vh">
          <q-toolbar-title>
            
            <q-avatar size="60px">
              <img :src="require(`./assets/logo.png`)"/>
            </q-avatar>
            BLOCKS
          </q-toolbar-title>
        </q-toolbar>
      </q-header>
      <!-- main body -->

      <q-page-container>
        <router-view />
      </q-page-container>

      <!-- footer  -->
      <q-footer reveal elevated>
        <q-toolbar class="bg-teal-4">
          
        </q-toolbar>
      </q-footer>


    </q-layout>
</template>

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
</style>
