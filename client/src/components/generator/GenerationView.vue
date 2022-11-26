<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="text-h1">We are currently generating the option blocks!</div>
        <div class="text-h4">Please be patient as it may take a few minutes</div>
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
    name: 'GenerationView',
    emits: ["back", "next"],
    props: ["usingDatabase", "optionsFile"],

    beforeMount() {
        var formData = new FormData()
        formData.append("data", this.optionsFile)
        const payload = {
            "data_using_csv": !this.usingDatabase,
            "code": this.$route.params.room_id,

        }
        formData.append("payload", JSON.stringify(payload))

        axiosInstance.post(`api-generate/generator/run/`, formData, {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }).then(
            response => {
                console.log(response);
                this.$emit("next")
            }
        )
    },

});
</script>
