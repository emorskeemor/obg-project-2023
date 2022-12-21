<template>
<q-card square flat>
    <div class="row justify-center">
        <div class="bg-grey-3" style="width:110vh">
            <div class="text-h4 row q-pa-sm">
                Successful students<div class="text-bold q-ml-sm">
                    <q-chip icon="account_circle">{{ this.$store.state.success_percentage }}%</q-chip>
                    <q-chip icon="account_circle">{{ Object.keys(this.$store.state.successful_students).length}}</q-chip>
                </div>
            </div>
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

    </div>

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
