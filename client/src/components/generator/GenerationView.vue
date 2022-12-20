<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <q-card class="absolute-center bg-grey-4 " style="min-height:50vh">
            <div v-if="run">
                <q-card-section>
                    <div class="text-h3">We are currently generating the option blocks!</div>
                </q-card-section>
                <q-card-section>
                    <div class="text-h4">Please be patient as it may take a few minutes</div>
                    <div class="text-h4">{{time}}</div>
                </q-card-section>
            </div>
            <div v-else>
                <q-card-section>
                    <div class="text-h3">Blocks have already been generated</div>
                </q-card-section>
            </div>
        </q-card>

    </q-card>
    <div class="absolute-bottom q-pa-sm" v-if="!run">
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

        }
    },

    beforeMount() {
        if (this.run === true) {
            this.toggleTimer()
            var formData = new FormData()
            formData.append("data", this.$store.state.data_file)
            console.log(!this.$store.state.using_database);
            const payload = {
                "data_using_csv": !this.$store.state.using_database,
                "code": this.$route.params.room_id,

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
    methods: {
        toggleTimer() {
            if (this.isRunning) {
                clearInterval(this.interval);
                console.log('timer stops');
            } else {
                this.interval = setInterval(this.incrementTime, 100);
            }
            this.isRunning = !this.isRunning
        },
        incrementTime() {
            this.time = Math.round((this.time + 0.10) * 100) / 100;
        },
    }

});
</script>
