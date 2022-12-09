<template>
    <div class="col" style="width:90px">
        <q-separator />
        <div class="text-h6 text-white">{{code}}</div>
    </div>
</template>
<script lang="js">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'OptionItem',  
    props: ["code"],
});

</script>