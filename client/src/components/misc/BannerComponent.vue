<template>
<div class="">
    <q-banner inline-actions :class="getType">
        <div class="absolute-center q-pa-md">
            <div class="text-bold">
                {{message}}
            </div>
        </div>
        <template v-slot:action>
            <q-btn flat color="white" @click="$emit('dismiss')" icon="close" />
        </template>
    </q-banner>
</div>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';

export default defineComponent({
    name: 'BannerComponent',
    props: ["colour", "message"],
    emits: ["dismiss"],
    computed: {
        getType() {
            return `text-white fixed-bottom q-pa-md z-max bg-${this.colour}`
        }
    }

});
</script>
