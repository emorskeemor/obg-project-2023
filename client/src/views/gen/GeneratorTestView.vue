<template>
    <q-layout view="lHr lpR lFr" class="shadow-2 rounded-borders">
        <q-page-container class="q-pa-xl absolute-center" style="width:500px" >
            <q-form @submit="handleLogin()" @reset="handleReset()" class="q-gutter-md">
            <h4>Data</h4>
            <q-file outlined v-model="data_file">
                <template v-slot:prepend>
                <q-icon name="attach_file" />
                </template>
            </q-file>
            <h4>Options</h4>
            <q-file outlined v-model="options_file">
                <template v-slot:prepend>
                <q-icon name="attach_file" />
                </template>
            </q-file>
            <div>
                <!-- <q-btn label="Submit" type="submit" color="primary"/>
                <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" /> -->
                <button type="submit">submit</button>
                <button type="reset">reset</button>
            </div>
            
            </q-form>
            <div v-if="results">
                {{results}}
            </div>

            <div v-if="results">
                <apexchart width="500" type="bar" :options="options" :series="series"></apexchart>
            </div>
            {{series}}
            {{options}}
            
        </q-page-container>
  </q-layout>

</template>

<script lang="ts">
import { defineComponent } from 'vue';

import { axiosInstance } from '@/api/axios'

export default defineComponent({
    name:"GeneratorTestView",
    data() {
        return {
            data_file: null,
            options_file: null,
            results:false,
            options: {
                chart: {
                id: 'vuechart-example'
                },
                xaxis: {
                categories: []
                }
            },
            series: [{
                name: 'series-1',
                data: []
            }]
        }
    },
    methods:{
        handleLogin(){
            console.log("submit");
            var formData = new FormData()
            if (this.data_file !== null && this.options_file !== null){
                formData.append("data", this.data_file)
                formData.append("options", this.options_file)
                axiosInstance.post("/generator/file/", formData, {
                    headers: { "Content-Type": "multipart/form-data" }
                }).then(res=>{
                    console.log(res);
                    
                    this.results = true
                    this.options.xaxis.categories = res.data.categories
                    for (let i=0; this.series.length; i ++) {
                        console.log(i);
                        
                        console.log(this.series[i]);
                        
                        if (this.series[i].name === "series-1"){
                            this.series[i].data = res.data.count
                        }
                    }
                    
                }).catch(err=>{
                    console.log(err);
                    
                })
            }
            
        },
        handleReset(){
            console.log("poop");
            
        }
    }
})
</script>