<template>
<q-card square>
    <q-card-section class="row justify-center">
        <div class="bg-grey-3" style="width:100vh">
            <div class="row justify-center items-center">
                <q-separator />
                <div class="col-2 q-pa-sm bg-grey-4 text-bold">ID</div>
                <div class="col-4 q-pa-sm bg-grey-4 text-bold">Name</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Pathway</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Options</div>
            </div>
            <div>
                <q-scroll-area style="height:70vh">
                    <div class="bg-grey-3 q-mb-xl" style="width:100vh">
                        <div v-for="(student, index) in $store.state.successful_students" :key="index">
                            <Student :student="student" :index="index" />
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
import Student from './Student.vue';


export default defineComponent({
    name: 'OptionItem',
    props: ["student", "index"],
    components: {
        Student
    }
});
</script>
