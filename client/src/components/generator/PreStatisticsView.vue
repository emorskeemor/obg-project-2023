<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-7 q-ma-lg">
                <q-card>
                    <q-card-section>
                        <div class="text-h4">Subject popularity</div>
                    </q-card-section>
                    <q-card-section>
                        <apexchart width="800" height="450" type="bar" :options="options" :series="series" v-if="!fetching"></apexchart>
                    </q-card-section>

                </q-card>
            </div>
            <div class="col-4 q-ma-lg">
                <q-card>
                    <div class="text-h4 q-pa-md">Student pathways</div>

                    <apexchart width="500" type="pie" :options="pathOptions" :series="pathSeries" v-if="!fetching"></apexchart>
                </q-card>
            </div>
        </div>
    </q-card>
    <div class="absolute-bottom q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>

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
    props: ["optionsFile", "usingDatabase"],

    beforeMount() {
        console.log(this.optionsFile);
        var formData = new FormData()
        formData.append("data", this.optionsFile)
        const payload = {
            "using_database": this.usingDatabase,
            "room_id": this.$route.params.room_id,

        }
        formData.append("payload", JSON.stringify(payload))

        axiosInstance.post(`api-generate/generator/pre-generate-statistics/`,
            formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            }).then(
            response => {
                console.log(response);

                this.options.xaxis.categories = response.data.subjects
                this.series[0].data = response.data.counts

                this.pathSeries = response.data.pathway_counts
                this.pathOptions.labels = response.data.pathways
                this.fetching = false

            }
        )
    },

    data() {
        return {
            // options for bar chart
            options: {
                chart: {
                    type: 'bar',
                    height: 600
                },
                plotOptions: {
                    bar: {
                        borderRadius: 4,
                        horizontal: true,
                    }
                },
                dataLabels: {
                    enabled: false
                },

                xaxis: {
                    categories: []
                },

            },
            series: [{
                name: 'series-1',
                data: []
            }],
            // options for pie chart
            pathSeries: [44, 55, 13, 43, 22],
            pathOptions: {
                chart: {
                    width: 380,
                    type: 'pie',
                },
                labels: ['Team A', 'Team B', 'Team C', 'Team D', 'Team E'],
                responsive: [{
                    breakpoint: 480,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }]
            },

            fetching: true,
        }
    },
    methods: {

    }

});
</script>
