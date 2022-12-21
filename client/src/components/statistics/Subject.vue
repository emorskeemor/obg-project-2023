<template>

<q-card class="bg-grey-2" style="padding:1px">
    <div class="text-black">{{code}}, {{this.$store.state.options[code]}}</div>

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
