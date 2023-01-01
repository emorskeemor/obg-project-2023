<template>
<q-card square flat class="bg-grey-3">
    <div class="row justify-center bg-grey-3">
        <div class="bg-grey-3" style="width:110vh">
            <div class="text-h4 row q-pa-sm">
                Failed students<div class="text-bold q-ml-sm">
                    <q-chip icon="account_circle">{{ Math.round(100-this.$store.state.success_percentage) }}%</q-chip>
                    <q-chip icon="account_circle">{{ Object.keys(this.$store.state.failed_students).length}}</q-chip>

                </div>
                <q-input filled v-model="search" label="Search for students" lazy-rules type="text" dense class="q-ml-xl"
                :disable="this.$store.state.using_database == false"
                >
                    <template v-slot:prepend>
                        <q-icon name="search" />
                    </template>
                </q-input>
            </div>
            <div class="row justify-center items-center">
                <q-separator />
                <div class="col-2 q-pa-sm bg-grey-4 text-bold">ID</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Name</div>
                <div class="col-2 q-pa-sm bg-grey-4 text-bold">Pathway</div>
                <div class="col-2 q-pa-sm bg-grey-4 text-bold">Options</div>
                <div class="col-3 q-pa-sm bg-grey-4 text-bold">Priority</div>
            </div>
            <div style="height:62vh"  class="bg-grey-4">
                <div class="bg-grey-3" style="width:100vh">
                    <div v-for="(student, index) in getFilteredOptions" :key="index">
                        <FailedStudent :student="student" :index="index" />
                    </div>
                    <div class="row justify-center absolute-bottom q-ma-sm">
                        <q-pagination v-model="page" :max=studentPagination :max-pages=4 direction-links push color="teal" active-design="push" active-color="red-5" />
                    </div>
                </div>
            </div>
        </div>

    </div>

</q-card>
</template>

<script lang="js">
import {
    defineComponent
} from 'vue';
import FailedStudent from './FailedStudent.vue';

const CHOSEN_OPTIONS_PER_PAGE = 10


export default defineComponent({
    name: 'OptionItem',
    props: ["student", "index"],
    components: {
        FailedStudent
    },
    data() {
        return {
            students: Object.values(this.$store.state.failed_students),
            search: "",
            page: 1
        }
    },
    computed: {
        studentPagination() {
            return Math.floor(this.students.length / CHOSEN_OPTIONS_PER_PAGE) + 1

        },
        getFilteredOptions() {
            // get chosen options through the search

            let startingPage = (this.page - 1) * CHOSEN_OPTIONS_PER_PAGE
            return [...[...this.students].filter(
                student => student.name.toLowerCase().includes(this.search.toLowerCase())
            )].slice(startingPage, startingPage + CHOSEN_OPTIONS_PER_PAGE)

        },
    },
});
</script>
