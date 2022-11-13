<template>
    <q-card>
        <q-card-section class="bg-teal-3 glossy">
        <div class="text-h6 text-white text-weight-bold">{{details.title}},{{details.subject_code}}</div>
        </q-card-section>

        <q-card-section class="q-pt-none q-pa-sm">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
        ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
        laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
        in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat 
        cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </q-card-section>

        <q-card-actions align="right">
        <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
    </q-card>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'SubjectInfoDialog',  
    props: ["details"],
    
});

</script>