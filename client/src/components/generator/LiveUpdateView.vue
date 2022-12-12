<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-8">
                <q-card square style="height:80vh">
                    <div class="row">
                        <div v-for="(i, index) in items" :key="i[0]" class="col q-ma-md">
                            <div class="text-h4">block {{index+1}}</div>
                            <draggable class="list-group" :list="items[index]" :id=i item-key="id" :group="{ name: 'people', pull: true, put: true }" :move="moveSubject" @start="tagSubject">
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
                        {{current}}
                    </q-card-section>
                    <q-card-section>

                    </q-card-section>
                    <q-separator />
                    <q-card-section>
                        <div class="text-h4">utilities</div>
                    </q-card-section>
                    <q-card-actions>
                        <q-btn-group>
                            <q-btn push class="bg-teal-4 text-white" size="md" label="evaluate" />
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

export default defineComponent({
    name: 'PreStatisticsView',
    emits: ["back", "next", "error", "dismissError"],
    components: {
        draggable
    },
    data() {
        return {
            items: [...this.$store.state.generated_blocks],
            current: "",
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
        tagSubject(arg) {
            this.current = arg.item.innerText
        },
    
    },

});
</script>
