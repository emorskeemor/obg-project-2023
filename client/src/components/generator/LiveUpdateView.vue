<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-8">
                <q-card square>
                    <q-card-section>
                        <div class="text-h4">Manipulate blocks</div>
                    </q-card-section>
                    <q-card-section>
                        <div class="row">
                            <div v-for="(i, index) in items" :key="i[0]" class="col q-ma-md">
                                <draggable class="list-group" :list="items[index]" :id=i item-key="id" :group="{ name: 'people', pull: true, put: true }" :move="moveSubject">
                                    <!-- iterate over all available options in pagination -->
                                    <template #item="{element}">
                                        <q-card class="bg-grey-4 q-pa-sm" square>

                                            {{element}}
                                        </q-card>
                                    </template>
                                </draggable>
                            </div>
                        </div>

                    </q-card-section>
                </q-card>

            </div>
            <div class="col-4">
                <q-card square>
                    <q-card-section>
                        <div class="text-h4">statistics</div>

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
            items: [...this.$store.state.generated_blocks]
        }
    },
    methods: {
        moveSubject(event, og) {
            console.log(event);
            if (event.relatedContext.list.includes(event.draggedContext.element) && event.from !== event.to) {
                this.$emit("error", `'${event.draggedContext.element}' already exists in this block`)
                return false
            }
        }
    },

});
</script>
