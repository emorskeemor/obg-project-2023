<template>

<q-card class="bg-grey-2" style="padding:3px">
    <div class="text-black main-font">{{code[0]}}, {{this.$store.state.options[code[0]]}}</div>

</q-card>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';

export default defineComponent({
    name: 'OptionItem',
    props: ["code"],
});
</script>
