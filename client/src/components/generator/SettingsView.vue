<template>
<div style="min-height:56vh">
    <q-card class="absolute-center bg-grey-3" style="width:100%;height:75%;" square>
        <div class="absolute-center">
            <q-card-section>
                <div class="main-font text-h3 text-weight-medium">
                    Ensure your settings are good to go!
                </div>
            </q-card-section>
            <q-card-section>
              
            </q-card-section>

        </div>
    </q-card>
    <div class="absolute-bottom-left q-pa-sm">
        <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
    </div>
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
    watch: {
        file() {
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
    methods: {
        // changeOpt(){
        //     if (this.usingDatabase === true){
        //         this.usingDatabase = false
        //     } else {
        //         this.usingDatabase = true
        //     }
        // }
    }

});
</script>
