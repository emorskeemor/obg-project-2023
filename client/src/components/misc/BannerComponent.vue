<template>
    <q-banner inline-actions :class="getType">
        <div class="absolute-center">
            {{message}}
        </div>
        <template v-slot:action>
            <q-btn flat color="white" label="Dissmis" @click="$emit('dismiss')"/>
        </template>
    </q-banner>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'BannerComponent',
    props: ["colour", "message"],
    emits: ["dismiss"],
    computed: {
        getType() {
            return `text-white absolute-bottom bg-${this.colour}`
        }
    }
  
});

</script>