<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-9">
                <q-card>
                    <q-card-section>
                        <div class="text-h4">Manipulate blocks</div>
                    </q-card-section>
                    <q-card-section>
                        <div class="row">
                            <div v-for="(i, index) in items" :key="i[0]" class="col q-ma-md">
                                <draggable class="list-group" :list="items[index]" :id=i item-key="id" :group="{ name: 'people', pull: true, put: true }">
                                    <!-- iterate over all available options in pagination -->
                                    <template #item="{element}">
                                        <div class="q-pa-sm bg-red">
                                            {{element}}
                                        </div>
                                    </template>
                                </draggable>
                            </div>
                        </div>
                    </q-card-section>
                </q-card>

            </div>
            <div class="col-3">
                <q-card>
                    {{items}}

                </q-card>
            </div>
        </div>

    </q-card>
    <div class="absolute-bottom-right q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>
    <div class="absolute-bottom q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="save" icon="undo" />
        </q-btn-group>
    </div>
    <!-- <div class="absolute-bottom q-pa-md">
        </div>

        <div class="absolute-bottom-right q-pa-sm">
        </div> -->
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
    emits: ["back", "next"],
    components: {
        draggable
    },
    data() {
        return {
            items: [...this.$store.state.generated_blocks]
        }
    }

});
</script>
