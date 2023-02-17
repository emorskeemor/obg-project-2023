<template>
    <q-card>
        <q-card-section class="bg-teal-3">
        <div class="text-h6 text-white text-weight-bold">{{details.title}},{{details.subject_code}}</div>
        </q-card-section>

        <q-card-section class="q-pt-none q-pa-sm" v-if="details.description.length > 0">
            {{ details.description }}
        </q-card-section>
        <q-card-section class="q-pt-none q-pa-sm main-font text-h6" v-else>
            A description is not available at the moment
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