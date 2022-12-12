<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-7 q-ma-lg">
                <q-card style="min-height:70vh">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div class="absolute-center">
                            <q-card-section>
                                <div class="text-h4">Subject popularity</div>
                            </q-card-section>
                            <q-card-section>
                                <apexchart :width="810" height="410" type="bar" :options="barChartOptions" :series="barChartSeries" v-if="!fetching"></apexchart>
                            </q-card-section>
                        </div>
                    </transition>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <div class="col-4 q-ma-lg">
                <q-card style="min-height:60vh">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div>
                            <div class="text-h4 q-pa-md">Student pathways</div>

                            <apexchart width="500" type="pie" :options="pieOptions" :series="pieSeries" v-if="!fetching"></apexchart>
                        </div>
                    </transition>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
        </div>
    </q-card>
    <div class="absolute-bottom-right q-pa-md">
        <div class="q-gutter-lg q-pa-md">
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-red text-white" size="md" label="Generate" icon="done" @click="$emit('next')" />
        </div>

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
    name: 'PreStatisticsView',
    emits: ["back", "next"],
    props: ["optionsFile", "usingDatabase"],

    beforeMount() {
        console.log(window.innerHeight);
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
                this.barChartOptions.xaxis.categories = response.data.subjects
                this.barChartSeries[0].data = response.data.counts

                this.pieSeries = response.data.pathway_counts
                this.pieOptions.labels = response.data.pathways
                this.fetching = false

            }
        )
    },
    mounted() {
        this.$nextTick(() => {
            window.addEventListener('resize', this.onResize);
        })
    },

    beforeUnmount() {
        window.removeEventListener('resize', this.onResize);
    },

    data() {
        return {
            windowHeight: window.innerHeight,
            // options for bar chart
            barChartOptions: {
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
            barChartSeries: [{
                name: 'subjects',
                data: []
            }],
            // options for pie chart
            pieSeries: [],
            pieOptions: {
                chart: {
                    width: 380,
                    type: 'pie',
                },
                labels: [],
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
        onResize() {
            this.windowHeight = window.innerHeight
        }
    }

});
</script>
