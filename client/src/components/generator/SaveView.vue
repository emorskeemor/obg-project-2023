<template>
<div>
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>


    </q-card>
    <q-dialog v-model="showPopup">
        <q-card>
            <q-card-section>
                <div class="text-h6 text-center main-font">Would you like to save these blocks?</div>
            </q-card-section>

            <q-card-section class="q-pt-none text-body1">
                <q-input label="title" v-model="title" :rules="[val=>val.length > 5 || 'title must be longer than 5 characters']"/>
            </q-card-section>

            <q-card-actions align="right">
                <q-btn label="RESTART" color="red" @click="restart" />
                <q-btn label="SAVE" color="primary" @click="saveBlocks" v-if="title.length > 5" />

            </q-card-actions>
        </q-card>
    </q-dialog>
    <div class="absolute-bottom q-pa-sm">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>
</div>
</template>

    
<script>
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';

export default defineComponent({
    name: 'SaveView',
    emits: ["back", "next"],
    data () {
        return {
            showPopup : true,
            title: ""
        }
    },

    methods: {
        saveBlocks() {
            axiosInstance.post(`api-generate/option-blocks/`, {
                blocks: this.$store.state.generated_blocks,
                code: this.$route.params.room_id,
                title: this.title
            }).then(response => {
                console.log(response);

            })
        },
        restart() {
            this.$router.push({
                "name": "room-edit",
                params: {
                    user_id: this.$route.params.user_id,
                    room_id: this.$route.params.room_id,
                }
            })
        }
    }

});
</script>
