<template>
<q-page padding>
    <div>
        
        <q-card style="width:90vh;height:50vh" class="absolute-center bg-grey-3 shadow-15" >
            <div class="row justify-center items-center full-height q-pa-md">
                <div class="main-font text-h1 text-weight-medium">
                    Are you a
                </div>
                <div class="q-gutter-md row justify-center">
                    <div class="col-4">
                        <q-btn size="40px" push @click="$router.push(`/room/join`)" icon="face" class="bg-cyan-4 text-white">
                            student
                        </q-btn>
                    </div>
                    <div class="col-2">
                        <div class="main-font text-h3 text-weight-medium q-mt-lg bg">
                            OR
                        </div>
                    </div>
                    <div class="col-4">
                        <q-btn size="40px" push @click="$router.push(`/auth/login`)" icon="badge" class="bg-cyan-4 text-white">
                            Teacher
                        </q-btn>
                    </div>

                </div>
            </div>

        </q-card>
    </div>

</q-page>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';
import {
    isLoggedIn
} from 'axios-jwt';

export default defineComponent({
    name: 'HomeView',

    created() {
        this.$watch(
            () => this.$route.params,
            () => {
                this.loggedIn = isLoggedIn()
            },
            // fetch the data when the view is created and the data is
            // already being observed
            {
                immediate: true
            }
        )
    },
    data() {
        return {
            loggedIn: isLoggedIn()
        }
    },
});
</script>
