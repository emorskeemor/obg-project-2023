<template>
<q-card>
    <q-card-section class="row justify-center">
        <div class="bg-grey-3" style="width:100vh">
            <div class="row justify-center items-center">
                <q-separator />
                <div class="col-1 q-pa-sm bg-grey-4 text-bold">ID</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Name</div>
                <div class="col-2 q-pa-sm bg-grey-4 text-bold">Pathway</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Options</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Priority</div>
            </div>
            <div>
                <q-scroll-area style="height:70vh">
                    <div class="bg-grey-3 q-mb-xl" style="width:100vh">
                        <div v-for="(student, index) in $store.state.failed_students" :key="index">
                            <FailedStudent :student="student" :index="index" />
                        </div>
                    </div>
                </q-scroll-area>
            </div>
        </div>

    </q-card-section>

</q-card>
</template>

    
<script lang="js">
import {
    defineComponent
} from 'vue';
import FailedStudent from './FailedStudent.vue';

export default defineComponent({
    name: 'OptionItem',
    props: ["student", "index"],
    components: {
        FailedStudent
    }
});
</script>
