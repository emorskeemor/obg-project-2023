<template>
<q-layout view="lHh Lpr lFf" class="animation-area">
    <!-- navigation bar content -->
    <ul class="box-area">
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
        <li></li>
    </ul>
    <q-header elevated>
        <q-toolbar class="bg-teal-5 glossy" style="min-height:9vh">
            <q-toolbar-title>
                <div class="absolute-center cursor-pointer q-hoverable row items-center">
                    <q-avatar size="60px" @click="returnHome" square class="q-pa-xs">
                        <img :src="require(`./assets/logo.png`)" />
                    </q-avatar>
                    <div class="main-font" @click="returnHome" >EDGBARROW</div>
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
    <q-ajax-bar ref="bar" position="bottom" color="green-8" size="10px" />

    <!-- footer  -->
    <q-footer reveal elevated>
        <q-toolbar class="bg-teal-5" style="height:7vh">
            <q-btn class="bg-black" @click="$router.back()">Back</q-btn>
        </q-toolbar>
    </q-footer>
</q-layout>
</template>

<script lang="ts">
import {
    defineComponent
} from 'vue';
import {
    getAccessToken,
    isLoggedIn
} from 'axios-jwt';
import {
    logout
} from './api/auth';

export default defineComponent({
    name: 'App',
    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.loggedIn = isLoggedIn()
            }, {
                immediate: true
            }
        )
    },
    data() {
        return {
            loggedIn: false
        }
    },
    methods: {
        handleLogout() {
            // logout the user by removing the access and refresh tokens from local
            // storage and then change the flag, once done redirect back to the home page
            logout()
            this.loggedIn = false
            this.$router.push({
                name: "home",
                force: true
            })
        },
        returnHome() {
            // check that the user is still logged in. We do this by gettings the access token if
            // it is still present. If not, we know the user is no longer logged in
            const accessToken = getAccessToken()
            if (accessToken) {
                logout()
            } else {
                this.$router.push({
                    name: "home"
                })

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


/* https://www.divinectorweb.com/2020/10/animated-background-html-css.html */
.animation-area {
    background: linear-gradient(to bottom, #93d6d6, #cbe5e7);
    width: 100%;
    height: 100vh;
}

.box-area {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 90%;
    overflow: hidden;
}

.box-area li {
    position: absolute;
    display: block;
    list-style: none;
    width: 25px;
    height: 25px;
    background: rgba(255, 255, 255, 0.2);
    animation: animate 20s linear infinite;
    bottom: -150px;
}

.box-area li:nth-child(1) {
    left: 86%;
    width: 80px;
    height: 80px;
    animation-delay: 0s;
}

.box-area li:nth-child(2) {
    left: 12%;
    width: 30px;
    height: 30px;
    animation-delay: 1.5s;
    animation-duration: 10s;
}

.box-area li:nth-child(3) {
    left: 70%;
    width: 100px;
    height: 100px;
    animation-delay: 5.5s;
}

.box-area li:nth-child(4) {
    left: 42%;
    width: 150px;
    height: 150px;
    animation-delay: 0s;
    animation-duration: 15s;
}

.box-area li:nth-child(5) {
    left: 65%;
    width: 40px;
    height: 40px;
    animation-delay: 0s;
}

.box-area li:nth-child(6) {
    left: 15%;
    width: 110px;
    height: 110px;
    animation-delay: 3.5s;
}

@keyframes animate {
    0% {
        transform: translateY(0) rotate(0deg);
        opacity: 1;
    }

    100% {
        transform: translateY(-800px) rotate(360deg);
        opacity: 0;
    }
}
</style>
