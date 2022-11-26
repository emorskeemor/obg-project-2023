<template>
    <div style="min-height:68vh">
        <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
            
    
        </q-card>
        <div class="absolute-bottom q-pa-sm">
            <q-btn-group>
                <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
                <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
            </q-btn-group>
        </div>
        <!-- <div class="absolute-bottom q-pa-md">
        </div>
    
        <div class="absolute-bottom-right q-pa-sm">
        </div> -->
    </div>
    </template>
    
    <script lang="ts">
    import {
        axiosInstance
    } from '@/api/axios';
    import {
        defineComponent,
        ref
    } from 'vue';
    
    export default defineComponent({
        name: 'PreStatisticsView',
        emits: ["back", "next"],
        

    
    });
    </script>
    