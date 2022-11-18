<template>
    <div style="min-height:48vh">
        <q-card class="absolute-center bg-grey-3 " style="width:80%;height: 80%;">
            <div class="absolute-center">
                <q-card-section>
                    <div class="main-font text-h3 text-weight-medium">
                        How should we get the student's options?
                    </div>
                </q-card-section>
                <q-card-section>
                    <div class="q-pa-md q-gutter-lg row justify-center items-center">
                        <div class="col-4">
                            <q-btn push icon="folder_open" class="bg-cyan-4 text-white" label="CSV" size="xl" />

                        </div>
                        <div class="col-1">
                            <div class="main-font text-h3 text-weight-medium absolute-center">
                                OR
                            </div>
                        </div>
                        <div class="col-4">
                            <q-btn push class="bg-cyan-4 text-white" size="xl" label="Database" />

                        </div>

                    </div>
                </q-card-section>
            </div>

        </q-card>
    </div>
</template>

<script lang="ts">
import {
    defineComponent
} from 'vue';

export default defineComponent({
    name: 'OptionsProivsionsView',

    data() {
        return {}
    },

});
</script>
