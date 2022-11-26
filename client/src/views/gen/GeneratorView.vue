<template>
<div>
    <q-stepper v-model="step" ref="stepper" color="primary" animated class="bg-grey-4">
        <q-step :name="1" title="Define data" icon="settings" :done="step > 1" :error="errorMessage.length !== 0">
            <OptionProvisionView @choose="handleOptions" @back="$refs.stepper.back()" />

        </q-step>

        <q-step :name="2" title="Settings" icon="settings" :done="step > 2">
            <SettingsView @back="backStep" @next="nextStep" />
        </q-step>

        <q-step :name="3" title="Pre-statistics" icon="assignment" :done="step > 3">
            <PreStatisticsView @back="backStep" @next="nextStep" :usingDatabase="usingDatabase" :optionsFile="optionsFile" />
        </q-step>

        <q-step :name="4" title="Generate" icon="add_comment" :done="step > 4">
            <GenerationView @back="backStep" @next="nextStep"  :usingDatabase="usingDatabase" :optionsFile="optionsFile" />

        </q-step>
        <q-step :name="5" title="Post-statistics" icon="assignment">
            <PostStatisticsView @back="backStep" @next="nextStep" />

        </q-step>
        <q-step :name="6" title="Live update" icon="add_comment">
            <LiveUpdateView @back="backStep" @next="nextStep" />

        </q-step>
        <q-step :name="7" title="Save" icon="add_comment">
            <SaveView @back="backStep" @next="nextStep" />

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
        }
    },
    methods: {
        handleOptions(usingDb, file) {
            console.log("hello!");
            if (usingDb === false) {
                if (file.type !== "text/csv") {
                    console.log("error raised");
                    this.errorMessage = "The file provided is not a CSV file."
                } else {
                    console.log("using csv");
                    this.usingDatabase = false
                    this.optionsFile = structuredClone(file)
                    console.log(this.optionsFile);
                    this.$refs.stepper.next()
                }
            } else {
                this.usingDatabase = true
                this.$refs.stepper.next()

            }
        },
        dismissError() {
            this.errorMessage = ""
        },
        nextStep() {
            this.$refs.stepper.next()
        },
        backStep() {
            this.$refs.stepper.previous()
        }
    },
})
</script>
