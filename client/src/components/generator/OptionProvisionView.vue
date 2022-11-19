<template>
<div style="min-height:63vh">
    <q-card class="absolute-center bg-grey-3" style="width:100%;height:80%;" square>
        <div class="absolute-center">
            <q-card-section>
                <div class="main-font text-h3 text-weight-medium">
                    How should we get the student's options?
                </div>
            </q-card-section>
            <q-card-section>
                <div class="q-pa-md q-gutter-lg row justify-center items-center">
                    <div class="col-4">
                        <q-btn push icon="folder_open" class="bg-cyan-4 text-white" label="CSV" size="xl" style="width:100%;height:10vh;" />
                        <q-popup-edit v-model="label" auto-save class="q-pa-lg">
                            <q-file color="cyan-4" v-model="file" label="click to upload csv">
                                <template v-slot:prepend>
                                    <q-icon name="attach_file" />
                                </template>
                            </q-file>
                        </q-popup-edit>
                    </div>
                    <div class="col-2">
                        <div class="main-font text-h2 text-weight-medium absolute-center">
                            OR
                        </div>
                    </div>
                    <div class="col-4">
                        <q-btn push class="bg-cyan-4 text-white" size="xl" label="Database" icon="storage" style="width:100%;height:10vh;" @click="$emit('choose', true)"/>
                    </div>

                </div>
            </q-card-section>

        </div>
    </q-card>
</div>
</template>

<script lang="ts">
import {
    defineComponent,
    ref
} from 'vue';

export default defineComponent({
    name: 'OptionsProivsionsView',
    emits: ["choose", "back"],
    watch:{
        file(){
            this.$emit("choose", this.file)            
        }
    },
    data() {
        return {
            label: ref("hello"),
            file: ref(null),
            usingDatabase: false,
        }
    },
});
</script>
