<template>
<div>

    <q-stepper v-model="step" ref="stepper" color="primary" animated class="bg-grey-4" style="height:10vh">
        <q-step :name="1" title="Define data" icon="settings" :done="step > 1" :error="errorMessage.length !== 0">
            <OptionProvisionView  @back="previousStep" @next="nextStep" @error="onError"/>

        </q-step>

        <q-step :name="2" title="Settings" icon="settings" :done="step > 2">
            <SettingsView @back="previousStep" @next="nextStep"/>
        </q-step>

        <q-step :name="3" title="Pre-statistics" icon="assignment" :done="step > 3">
            <PreStatisticsView @back="previousStep" @next="nextStep" :usingDatabase="usingDatabase" :optionsFile="optionsFile" />
        </q-step>

        <q-step :name="4" title="Generate" icon="add_comment" :done="step > 4">
            <GenerationView @back="previousStep" @next="nextStep" :usingDatabase="usingDatabase" :optionsFile="optionsFile" :run="!finishedGeneration" @finished="generateCompleted" />

        </q-step>
        <q-step :name="5" title="Post-statistics" icon="assignment">
            <PostStatisticsView @back="previousStep" @next="nextStep" />

        </q-step>
        <q-step :name="6" title="Live update" icon="add_comment">
            <LiveUpdateView @back="previousStep" @next="nextStep" @error="onError" @dismissError="dismissError"/>

        </q-step>
        <q-step :name="7" title="Save" icon="add_comment">
            <SaveView @back="previousStep" @next="nextStep" />

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
import SaveView from '@/components/generator/SaveView.vue';

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
        SaveView
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
        onError(message){
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
