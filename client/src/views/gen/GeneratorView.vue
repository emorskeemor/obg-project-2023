<template>
<div class="q-ma-lg">
    <q-stepper v-model="step" ref="stepper" color="primary" animated class="bg-grey-4">
        <q-step :name="1" title="Define data" icon="settings" :done="step > 1">
            <OptionProvisionView @choose="handleOptions" @back="$refs.stepper.back()" />

        </q-step>

        <q-step :name="2" title="Settings" icon="settings" :done="step > 2">
            <SettingsView @back="$refs.stepper.previous()" />

        </q-step>

        <q-step :name="3" title="Pre-statistics" icon="assignment" :done="step > 3">
            This step won't show up because it is disabled.
        </q-step>

        <q-step :name="4" title="Generate" icon="add_comment">
        </q-step>
        <q-step :name="5" title="Post-statistics" icon="assignment">
        </q-step>
        <q-step :name="6" title="Live update" icon="add_comment">
        </q-step>
        <q-step :name="7" title="Save" icon="add_comment">
        </q-step>
    </q-stepper>
</div>
</template>

<script lang="js">
import OptionProvisionView from '@/components/generator/OptionProvisionView.vue';
import SettingsView from '@/components/generator/SettingsView.vue';
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
        SettingsView
    },
    data() {
        return {
            step: ref(1),
            // providing the data
            dataProvisionType: "csv",
        }
    },
    methods: {
        handleOptions() {
            console.log("uo");
            this.$refs.stepper.next()
        }
    },
})
</script>
