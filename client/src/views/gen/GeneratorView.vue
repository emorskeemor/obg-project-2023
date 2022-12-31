<template>
<div class="no-scroll">

    <q-stepper v-model="step" ref="stepper" color="primary" animated class="bg-grey-3 no-scroll" style="height:90vh">
        <q-step :name="1" title="Define data" icon="folder_open" :done="step > 1" :error="errorMessage.length !== 0">
            <OptionProvisionView @back="previousStep" @next="nextStep" @error="onError" />

        </q-step>

        <q-step :name="2" title="Settings" icon="settings" :done="step > 2">
            <SettingsView @back="previousStep" @next="nextStep" />
        </q-step>

        <q-step :name="3" title="Pre-statistics" icon="analytics" :done="step > 3">
            <PreStatisticsView @back="previousStep" @next="nextStep" :usingDatabase="usingDatabase" :optionsFile="optionsFile" :finished="finishedGeneration" />
        </q-step>

        <q-step :name="4" title="Generate" icon="grid_view" :done="step > 4" v-if="!finishedGeneration">
            <GenerationView @back="previousStep" @next="nextStep" :usingDatabase="usingDatabase" :optionsFile="optionsFile" :run="!finishedGeneration" @finished="generateCompleted" />

        </q-step>
        <q-step :name="5" title="Post-statistics" icon="trending_up" :done="step > 5">
            <PostStatisticsView @back="previousStep" @next="nextStep" />

        </q-step>
        <q-step :name="6" title="Live update" icon="update" :done="step > 6">
            <LiveUpdateView @back="previousStep" @next="nextStep" @error="onError" @dismissError="dismissError" />

        </q-step>

    </q-stepper>

    <BannerComponent colour="red" @dismiss="dismissError" v-if="errorMessage" :message="errorMessage" />

</div>
</template>

<script lang="js">
// views
import OptionProvisionView from '@/components/generator/OptionProvisionView.vue';
import SettingsView from '@/components/generator/SettingsView.vue';
import PreStatisticsView from '@/components/generator/PreStatisticsView.vue';
import PostStatisticsView from '@/components/generator/PostStatisticsView.vue';
import GenerationView from '@/components/generator/GenerationView.vue';
import LiveUpdateView from '@/components/generator/LiveUpdateView.vue';

import BannerComponent from '@/components/misc/BannerComponent.vue';
import {
    defineComponent
} from 'vue';
import {
    ref
} from 'vue'
import {
    axiosInstance
} from '@/api/axios';

export default defineComponent({
    name: "GeneratorView",
    components: {
        OptionProvisionView,
        SettingsView,
        BannerComponent,
        PreStatisticsView,
        PostStatisticsView,
        GenerationView,
        LiveUpdateView,
    },
    data() {
        return {
            step: ref(1),
            // providing the data
            usingDatabase: true,
            optionsFile: ref(null),
            errorMessage: "",
            generatedData: {},
            finishedGeneration: false,
        }
    },
    beforeRouteLeave(to, from, next) {
        const answer = window.confirm('Are you sure you want to exit the generation process?')
        if (answer) {
            next()
        } else {
            next(false)
        }

    },
    methods: {

        dismissError() {
            this.errorMessage = ""
        },
        nextStep() {
            this.dismissError()
            this.$refs.stepper.next()
        },
        previousStep() {
            this.dismissError()
            this.$refs.stepper.previous()
        },
        onError(message) {
            this.errorMessage = message
        },

        generateCompleted(data) {
            this.finishedGeneration = true
            this.generatedData = data
            console.log(this.generatedData);
            this.nextStep()
        }
    },
})
</script>
