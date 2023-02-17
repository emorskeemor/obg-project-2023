<template>
    <q-card>
        <q-card-section class="bg-teal-3">
            <div class="text-h6 text-white text-weight-bold">Pathway information</div>
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm text-weight-bold">
            Path one
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm">
            Students who wish to follow a more academic path of Alevels followed by university. This
            pathway maintains access to all career paths.

            Students must pick Geography or History (or both), a language and then have two free choices.
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm text-weight-bold">
            Path two
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm">
            Students whose career path is supported by vocational options. At the end of key
            stage 4, they would consider a vocational course or workrelated learning.

            Agreed by the student’s Form Tutor. Students must still pick one EBacc subject (geography, history, 
            triple science, computer science, or a language), a vocational subject and then have two free choices.
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm text-weight-bold">
            Path three
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm">
            Students who have additional needs for whom four options may create a work overload. 

            Students are invited to follow this path by our SENCO and Head of Year. Students should aim 
            for one EBacc subject and then have two free choices. The fourth option is supervised
            study.
        </q-card-section>
        <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
    </q-card>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'HelpDialog',  
    
});

</script>