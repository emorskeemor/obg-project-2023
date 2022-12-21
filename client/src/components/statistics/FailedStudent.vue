<template>
    <q-card class="bg-grey-3" style="width:110vh" square>
        <div class="row justify-center">
            <q-separator />
            <div class="col-2 q-pa-sm bg-grey-4">
                <q-btn color="grey" :label="index.slice(0,12)" size="sm">
                <q-popup-proxy>
                    <q-banner>
                        <template v-slot:avatar>
                            <q-icon name="account_circle" color="light-grey" />
                        </template>
                        <div class="row">
                            student uuid: {{index}}
                        </div>
                        <div class="row">
                            student email: {{student.email }}
                        </div>
                    </q-banner>
                </q-popup-proxy>
            </q-btn>
            </div>
    
            <div class="col-3 q-pa-sm">
                {{student.name}}
            </div>
            <div class="col-2 q-pa-sm">
                {{student.pathway}}
            </div>
    
            <div class="col-2 bg-grey-3">
                <div class="row float-right">
                    <div v-for="(option) in student.initial_options" :key="option">
                        <div class="q-pa-sm" style="width:3vh">
                            {{option}}
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-3">
                <div v-if="student.priorities" class="row float-right">
                    <div v-for="(option) in student.priorities" :key="option">
                        <div :class="getOptionStyle(option[1]-1)" style="width:6vh">
    
                            {{option[0]}}
                        </div>
                    </div>
                </div>
            </div>
            <!-- {{student}} -->
        </div>
    </q-card>
    </template>
    
    <script lang="js">
    import {
        defineComponent
    } from 'vue';
    
    export default defineComponent({
        name: 'OptionItem',
        props: ["student", "index"],
        data() {
            return {
                base: "bg-yellow",
                colours: ["bg-red", "bg-orange", "bg-yellow", "bg-green"]
            }
        },
        methods: {
            getOptionStyle(index){
                let base = "q-pa-sm "
                base = base.concat(this.colours[index])
                return base
            }
        }
    });
    </script>
    