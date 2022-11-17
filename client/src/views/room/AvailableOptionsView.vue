<template>
<q-page class="q-pa-xs no-scroll" padding>
    <!-- header  -->
    <q-card style="width:100vh;padding:5vh" class="absolute-center bg-grey-3">
        
    </q-card>
    <q-banner inline-actions class="text-white bg-red absolute-bottom" v-if="errorMessage.length!==0">
        <div class="absolute-center">
            {{errorMessage}}
        </div>
        <template v-slot:action>
            <q-btn flat color="white" label="Dissmis" @click="errorMessage=''" />
        </template>
    </q-banner>
</q-page>
</template>

    
<script lang="ts">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent
} from 'vue';

export default defineComponent({
    name: 'AvailableOptionsView',
    data() {
        // define variables
        return {
            roomCode: "",
            domainName: "",
            // errors
            error: false,
            errorMessage: "",

        }
    },
    methods:{
        getOptions() {
            // axiosInstance.get(`api-rooms/rooms/${this.$route.params.}/available_options`)
        }
    }
    
});
</script>
