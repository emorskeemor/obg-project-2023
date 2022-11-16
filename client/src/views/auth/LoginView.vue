<template>
<q-page class="q-pa-xl absolute-center" style="width:500px" padding>
    <h1 class="text-h2">Teacher login</h1>
    <q-form @submit="handleLogin()" @reset="handleReset()" class="q-gutter-md">
        <q-input filled v-model="email" label="Your email *" hint="email" lazy-rules type="email" :error="error">
            <template v-slot:prepend>
                <q-icon name="mail" />
            </template>
        </q-input>

        <q-input filled v-model="password" label="Your password *" hint="password" lazy-rules type="password" autocomplete="on" error-message="Password or username was invalid" :error="error">
            <template v-slot:prepend>
                <q-icon name="password" />
            </template>
        </q-input>
        <div class="q-gutter-md">
            <q-btn class="bg-green-13 text-white" push size="20px" @click="handleLogin">
                Login
            </q-btn>
            <q-btn class="bg-red-13 text-white" push size="20px" @click="handleReset">
                Reset
            </q-btn>
        </div>
    </q-form>
</q-page>
</template>

<script lang="ts">
import {
    defineComponent
} from 'vue';
import {
    login, logout
} from '@/api/auth'
import jwt_decode from 'jwt-decode'
import {
    DecodedTokenObject
} from '@/api/interfaces'
import {
    isLoggedIn
} from 'axios-jwt';

export default defineComponent({
    name: "LoginView",
    data() {
        return {
            password: "",
            email: "",
            error: false
        }
    },
    methods: {
        handleLogin() {

            login({
                'email': this.email,
                'password': this.password
            }).then(
                accessToken => {
                    const decoded: DecodedTokenObject = jwt_decode(accessToken)

                    console.log("successful login");
                    this.$router.push({
                        name: "user-dashboard",
                        params: {
                            user_id: decoded.user_id
                        }
                    })

                }
            ).catch(err => {
                this.$data.error = true
            })

        },
        handleReset() {
            this.password = ""
            this.email = ""
            this.error = false
        }
    },
    beforeRouteEnter(to, from, next) {
      
        if (isLoggedIn()) {
            const answer = window.confirm('You are already logged in! Returning to the login page will log you out')
            if (answer) {
                logout()
                next()
            } else {
                next(false)
            }
        }
      next()
    }
})
</script>
