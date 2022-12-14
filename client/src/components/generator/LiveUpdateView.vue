<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-8">
                <q-card square style="height:80vh">
                    <div class="row">
                        <div v-for="(i, index) in blocks" :key="i[0]" class="col q-ma-md">
                            <div class="text-h4">block {{index+1}}</div>
                            <draggable 
                            class="list-group" 
                            :list="blocks[index]" 
                            :id=index item-key="id" 
                            :group="{ name: 'people', pull: true, put: true }" 
                            :move="moveSubject" 
                            @start="startMove" @change="changeSubject" @end="finishedMove">
                                <!-- iterate over all available options in pagination -->
                                <template #item="{element}">
                                    <div>
                                        <q-card :class="current == element ? 'bg-red-6 q-pa-sm' : 'bg-grey-4 q-pa-sm'" @click="current=element">
                                            {{element}}
                                        </q-card> 
                                    </div>
                                </template>
                            </draggable>
                        </div>
                    </div>
                </q-card>
            </div>
            <div class="col-4">
                <q-card square style="height:80vh">
                    <q-card-section>
                        <div class="text-h4">statistics</div>
                        <!-- {{this.$store.state.all_students}} -->
                        {{this.operations}}
                    </q-card-section>
                    <q-card-section>

                    </q-card-section>
                    <q-separator />
                    <q-card-section>
                        <div class="text-h4">utilities</div>
                    </q-card-section>
                    <q-card-actions>
                        <q-btn-group>
                            <q-btn push class="bg-teal-4 text-white" size="md" label="evaluate" @click="evaluate" />
                        </q-btn-group>
                    </q-card-actions>
                </q-card>
            </div>
        </div>

    </q-card>
    <div class="absolute-bottom-right q-pa-md">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>
    <!-- <div class="absolute-bottom q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="save" icon="undo" />
        </q-btn-group> -->
    <!-- </div> -->
</div>
</template>

<script lang="js">
import draggable from "vuedraggable";

import {
    defineComponent,
    ref
} from 'vue';
import { axiosInstance } from "@/api/axios";

export default defineComponent({
    name: 'PreStatisticsView',
    emits: ["back", "next", "error", "dismissError"],
    components: {
        draggable
    },
    data() {
        return {
            blocks: this.$store.state.generated_blocks.map(function(arr) {return arr.slice();}),     
            current: "",
            operations: []
        }
    },
    methods: {
        moveSubject(event, og) {
            console.log("hello");
            if (event.relatedContext.list.includes(event.draggedContext.element) && event.from !== event.to) {
                this.$emit("error", `'${event.draggedContext.element}' already exists in this block`)
                return false
            }
        },
        changeSubject(event){
            console.log(event);
        },
        startMove(arg) {
            this.current = arg.item.innerText
        },
        finishedMove(event){
            console.log(event);
            this.operations.push({from:event.from.id, subject:event.item.innerText, to:event.to.id})
        },
        evaluate(){
            axiosInstance.post("api-generate/generator/evaluate/", {
                initial:this.$store.state.generated_blocks,
                // successful_students:this.$store.state.successful_students,
                // failed_students:this.$store.state.failed_students,
                all_students:this.$store.state.all_students,
                new:this.blocks
            }).then(response=>{
                console.log(response);
            })
        }
    },

});
</script>
