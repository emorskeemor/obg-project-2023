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
                <div class="text-h4 text-center main-font">Choose a protocol</div>

            </q-card-section>

            <q-card-section class="q-pt-none text-body1 main-font text-center">
                <div>
                    A protocol defines how the blocks will be generated
                </div>
                <q-card class="bg-grey-4 q-ma-md q-pa-sm">
                    <div v-if="protocol == `protocol B`" class="text-body2">
                        Almost exactly the same as protocol A but will order the option codes.
                    </div>
                    <div v-else-if="protocol == `protocol C`" class="text-body2">
                        Takes a significantly longer time than protocl B but will ensure certain uncertainties during
                        generation are dealt with
                    </div>
                    <div v-else-if="protocol == `protocol D`" class="text-body2">
                        Evaluates option blocks as soon as they have been generated and terminates when a set of blocks
                        reach a certain success percentage.
                    </div>
                    <div v-else-if="protocol == `protocol E`" class="text-body2">
                    </div>
                    <div v-else-if="protocol == `protocol A`" class="text-body2">
                        Default protocol. Generally the quickest protocol and will get the job done under 30 seconds. However,
                        there are many uncertainties and does not guarantee the best set of blocks.
                    </div>

                </q-card>
                <!-- show inputs based on the protocol being used -->
                <q-toggle v-if="protocol == `protocol B` " label="reverse options" v-model="reverseOptions" />
                <q-toggle v-if="protocol == `protocol C` " label="order options " v-model="orderOptions" />
                <q-input v-if="protocol == `protocol D` " label="target percentage" v-model="targetPercentage" class="q-ma-sm" />
                <q-input v-if="protocol == `protocol E`" label="iterations" v-model="iterations" class="q-ma-sm" />
                <q-select v-model="protocol" :options="availableProtocols" label="Choose a protocol" dense map-options class="q-pa-sm" />
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
            protocol: "protocol A",
            availableProtocols: [
                "protocol A",
                "protocol B",
                "protocol C",
                "protocol D",
                "protocol E",
            ],
            reverseOptions: true,
            targetPercentage: 90,
            iterations: 3,
            orderOptions: true

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
                    "protocol": this.protocol,
                    "reverse_options": this.reverseOptions,
                    "target_percentage": this.targetPercentage,
                    "iterations": this.iterations,
                    "order_options": this.orderOptions

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
                ).catch(error=> {
                    if (error.response.status=="500") {
                        this.$router.push({
                                name: "E500"
                            })
                    }
                })
            }
        },
    }

});
</script>
