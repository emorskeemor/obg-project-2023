<template>
<q-card style="min-width: 100vh" class="q-pa-md">
    <div class="text-h5 text-center main-font text-weight-medium">{{ data.title }}/{{ data.room.code }}

    </div>
    <div class="row">
        <q-chip icon="grid_view"># blocks : {{ data.number_of_blocks }}</q-chip>
        <q-chip icon="done">success % : {{ data.success_percentage }}</q-chip>
        <q-chip icon="category">completed nodes : {{ data.completed_nodes }}</q-chip>
        <q-chip icon="category">generated nodes : {{ data.generated_nodes }}</q-chip>
        <q-chip icon="schedule">generation time : {{ data.generation_time }} seconds</q-chip>
    </div>
    <q-card-section class="q-gutter-md">
        <q-scroll-area style="height:75vh">
            <q-card square class="q-pa-md bg-grey-4" flat>
                <div class="row justify-center">
                    <div v-for="(block, index) in data.blocks" :key="index">
                        <q-card style="width:80vh;min-height:15vh">
                            <div class="row">
                                <div class="col bg-grey-3" style="min-height:15vh">
                                    <div class="text-h6 text-black q-pa-sm row">Block<div class="text-bold q-ml-sm">[{{index+1}}] </div>
                                        <q-chip icon="subject">{{ block.length }}</q-chip>
                                    </div>
                                </div>
                                <div class="col-10">
                                    <div class="row q-pa-sm">
                                        <div v-for="code in block" :key="code" style="padding:5px">
                                            <q-card class="bg-grey-2" style="padding:3px">
                                                <div class="text-black main-font">
                                                    <b>{{code[0]}} </b>
                                                    {{ code[1] }}
                                                    <q-badge>
                                                        {{ code[2] }}
                                                    </q-badge>
                                                </div>

                                            </q-card>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </q-card>
                    </div>
                </div>
            </q-card>
        </q-scroll-area>
    </q-card-section>

</q-card>
</template>

<script>
import {
    defineComponent
} from 'vue';

export default defineComponent({
    name: "ResultsPopup",
    props: ["data"]

})
</script>
