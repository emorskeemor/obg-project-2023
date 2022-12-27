<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height">
        <q-card class="absolute-center bg-grey-5" style="height:50vh;width:50%" bordered>
            <div v-if="run" class="absolute-center">
                <div class="text-h4">We are currently generating the option blocks!</div>

                <div class="text-h6 ">Please be patient as it may take a few minutes</div>
                <div class="text-h5">seconds : {{time}}</div>
            </div>
            <div v-else>
                <div class="absolute-center text-h4">Blocks have already been generated</div>
            </div>
        </q-card>

    </q-card>
    <q-dialog v-model="wait" v-if="this.run" persistent>
        <q-card style="width:60vh">
            <q-card-section>
                <div class="text-h6 text-center">Choose a protocol</div>

            </q-card-section>

            <q-card-section class="q-pt-none text-body1">
                <div>
                    A protocol defines how the blocks will be generated
                </div>
                <q-select v-model="protocol" 
                    :options="availableProtocols" label="Choose a protocol" dense map-options class="q-pa-sm" />
            </q-card-section>

            <q-card-actions align="right">
                <q-btn push class="bg-teal-4 text-white" size="md" label="cancel" icon="cancel" @click="$emit('back')" />
                <q-btn push label="run" color="primary" @click="start" v-close-popup v-if="protocol!==null" />
            </q-card-actions>
        </q-card>
    </q-dialog>
    <div class="absolute-bottom q-pa-sm" v-if="!run">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>
</div>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';

export default defineComponent({
    name: 'GenerationView',
    emits: ["back", "next", "finished"],
    props: ["usingDatabase", "optionsFile", "run"],
    data() {
        return {
            time: 0,
            isRunning: false,
            interval: 0,
            wait: true,
            protocol: null,
            availableProtocols: [
                "protocol_A",
                "protocol_B",
                "protocol_C",
                "protocol_D",
                "protocol_E",
            ]

        }
    },

    methods: {
        toggleTimer() {
            if (this.isRunning) {
                clearInterval(this.interval);
            } else {
                this.interval = setInterval(this.incrementTime, 100);
            }
            this.isRunning = !this.isRunning
        },
        incrementTime() {
            this.time = Math.round((this.time + 0.10) * 100) / 100;
        },
        start() {
            if (this.run === true & this.protocol !== null) {
                this.toggleTimer()
                var formData = new FormData()
                formData.append("data", this.$store.state.data_file)

                const payload = {
                    "data_using_csv": !this.$store.state.using_database,
                    "code": this.$route.params.room_id,
                    "protocol": this.protocol

                }
                formData.append("payload", JSON.stringify(payload))

                axiosInstance.post(`api-generate/generator/run/`, formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }).then(
                    response => {
                        this.toggleTimer()
                        this.$store.commit("setEvaluation", response.data)
                        this.$emit("finished", response.data)
                    }
                )
            }
        },
    }

});
</script>
