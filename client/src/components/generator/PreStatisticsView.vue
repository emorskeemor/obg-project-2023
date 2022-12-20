<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row ">
            <div class="col-5 q-ma-md">
                <q-card style="min-height:72vh">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div class="q-pa-lg">
                            <!-- <div class="text-h6 q-pa-md">clashes</div> -->

                            <apexchart class="col" width="600" height="450" type="bar" :options="barChartOptions" :series="barChartSeries" v-if="!fetching"></apexchart>

                        </div>
                    </transition>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <div class="col q-ma-md">
                <q-card style="min-height:72vh">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div class="q-pa-lg">
                            <apexchart type="heatmap" height="350" width="350" :options="heatMapOptions" :series="heatMapSeries"></apexchart>
                            <div class="row">
                                <div class="col">
                                    <q-select v-model="ignoreOptions" style="width:20vh" multiple :options="availableOptions" use-chips stack-label label="ignore subjects" dense hint="select subjects to ignore" />

                                </div>
                                <div class="col">
                                    <q-input v-model="maxClashes" label="max clashes" dense type="number" />
                                    <q-input v-model="classes" label="classes" dense type="number" />
                                </div>
                            </div>
                        </div>
                    </transition>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
            <div class="col q-ma-md">
                <q-card style="min-height:50vh">
                    <transition appear enter-active-class="animated fadeIn" leave-active-class="animated fadeOut">
                        <div class="q-pa-sm">
                            <apexchart width="400" type="donut" :options="pieOptions" :series="pieSeries" v-if="!fetching"></apexchart>
                        </div>
                    </transition>
                    <q-inner-loading :showing="fetching" label="Please wait..." label-class="text-teal" />

                </q-card>
            </div>
        </div>
    </q-card>
    <div class="absolute-bottom-right q-pa-md">
        <div class="q-gutter-sm q-pa-sm">
            <q-btn label="refresh" size="md" @click="getData" color="teal-4" push/>
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
    props: [],

    beforeMount() {
        this.getData()
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
            // OPTIONS FOR BAR CHART
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
                title: {
                    text: 'Subject popularity',
                    align: 'center'
                },

            },
            barChartSeries: [{
                name: 'subjects',
                data: []
            }],
            // PATHWAY PIE CHART
            pieSeries: [],
            pieOptions: {
                chart: {
                    width: 380,
                    type: 'pie',
                },
                labels: [],
                responsive: [{
                    breakpoint: 200,
                    options: {
                        chart: {
                            width: 200
                        },
                        legend: {
                            position: 'bottom'
                        }
                    }
                }],
                title: {
                    text: 'Pathways chosen by students',
                    align: 'center'
                },
                dataLabels:{
                    enabled:false
                }
            },
            // CLASH HEAT MAP
            heatMapSeries: [],
            heatMapOptions: {
                chart: {
                    height: 500,
                    type: 'heatmap',
                },
                dataLabels: {
                    enabled: false
                },
                colors: ["#008FFB"],
                title: {
                    text: 'Subject clashes'
                },
            },
            // OTHER DATA
            ignoreOptions: [],
            availableOptions: [],
            classes: 1,
            maxClashes: 3,

            fetching: true,
        }
    },
    methods: {
        onResize() {
            this.windowHeight = window.innerHeight
        },
        getData() {
            this.fetching = true
            var formData = new FormData()
            formData.append("data", this.$store.state.data_file)
            const payload = {
                "using_database": this.$store.state.using_database,
                "room_id": this.$route.params.room_id,
                "ignore_subjects": this.ignoreOptions,
                "classes": this.classes,
                "max_clashes": this.maxClashes
            }
            formData.append("payload", JSON.stringify(payload))

            axiosInstance.post(`api-generate/generator/pre-generate-statistics/`,
                formData, {
                    headers: {
                        "Content-Type": "multipart/form-data"
                    }
                }).then(
                response => {
                    this.$store.commit("setPreStatistics", response.data)
                    let data = response.data
                    // popularity bar chart
                    this.barChartOptions.xaxis.categories = data.popularity_bar_chart.options
                    this.barChartSeries[0].data = data.popularity_bar_chart.series
                    // pie chart
                    this.pieSeries = data.pathway_pie_chart.series
                    this.pieOptions.labels = data.pathway_pie_chart.options
                    // clash heat map
                    this.heatMapSeries = data.clash_heat_map.series

                    this.availableOptions = data.subject_codes
                    this.fetching = false

                }
            )
        },
    }

});
</script>
