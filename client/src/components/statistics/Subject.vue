<template>
<!-- <div style="width:5vh" class="bg-red">
    <div class="text-h6 text-white">{{code}}</div>

</div> -->
<q-card class="bg-grey-2" style="width:5vh">
    <div class="text-h6 text-black">{{code}}</div>

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
