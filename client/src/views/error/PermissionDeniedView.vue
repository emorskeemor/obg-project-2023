<template>
    <q-page padding>
        <h1><q-icon name="error"/></h1>
        <h3>401 Permission Denied</h3>
        <h4>You cannot access this resource</h4>
        <h6>Maybe try again later, but its probably best not to</h6>
    </q-page>
</template>
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name:"PermissionDenied",

})
</script>