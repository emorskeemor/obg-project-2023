<template>
    <q-page padding>
        <h1><q-icon name="error"/></h1>
        <h3>500</h3>
        <h4>There seems to be an error on our end</h4>
        <h6>Maybe try again later</h6>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name:"ServerError",

})
</script>