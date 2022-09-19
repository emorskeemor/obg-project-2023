<template>
    <q-page padding>
        <h1><q-icon name="error"/></h1>
        <h3>404</h3>
        <h4>Unfortunately we could not find what you were looking for</h4>
        <h6>Maybe try again later, or not, up to you</h6>
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name:"ResourceNotFound",

})
</script>