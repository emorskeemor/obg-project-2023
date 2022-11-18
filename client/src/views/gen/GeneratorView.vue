<template>
<div class="q-pa-xl">
    <q-stepper v-model="step" ref="stepper" color="primary" animated class="bg-grey-4">
        <q-step :name="1" title="Define data to be used" icon="settings" :done="step > 1">
            <OptionProvisionView />
        </q-step>

        <q-step :name="2" title="Settings" caption="Optional" icon="create_new_folder" :done="step > 2">
            An ad group contains one or more ads which target a shared set of keywords.
        </q-step>

        <q-step :name="3" title="Ad template" icon="assignment" :done="step > 3">
            This step won't show up because it is disabled.
        </q-step>

        <q-step :name="4" title="Create an ad" icon="add_comment">
            Try out different ad text to see what brings in the most customers, and learn how to
            enhance your ads using features like ad extensions. If you run into any problems with
            your ads, find out how to tell if they're running and how to resolve approval issues.
        </q-step>

        <template v-slot:navigation>
            <q-stepper-navigation>
                <q-btn @click="$refs.stepper.next()" color="primary" :label="step === 4 ? 'Finish' : 'Continue'" />
                <q-btn v-if="step > 1" flat color="primary" @click="$refs.stepper.previous()" label="Back" class="q-ml-sm" />
            </q-stepper-navigation>
        </template>
    </q-stepper>
</div>
</template>

<script lang="js">
import OptionProvisionView from '@/components/generator/OptionProvisionView.vue';
import {
    defineComponent
} from 'vue';
import {
    ref
} from 'vue'

export default defineComponent({
    name: "GeneratorView",
    components: {
        OptionProvisionView
    },
    data() {
        return {
            step: ref(1)
        }
    }
})
</script>
