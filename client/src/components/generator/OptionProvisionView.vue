<template>
<div style="min-height:68vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="absolute-center">
            <q-card-section>
                <div class="main-font text-h3 text-weight-medium">
                    How should we get the student's options?
                </div>
            </q-card-section>
            <q-card-section>
                <div class="q-pa-md q-gutter-lg row justify-center items-center">
                    <div class="col-4">
                        <q-btn push icon="folder_open" class="bg-cyan-4 text-white" label="CSV" size="xl" style="width:100%;height:10vh;" />
                        <q-popup-edit v-model="label" auto-save class="q-pa-lg">
                            <q-file color="cyan-4" v-model="file" label="click to upload csv" style="width:30vh">
                                <template v-slot:prepend>
                                    <q-icon name="attach_file" />
                                </template>
                            </q-file>
                        </q-popup-edit>
                    </div>
                    <div class="col-2">
                        <div class="main-font text-h2 text-weight-medium absolute-center">
                            OR
                        </div>
                    </div>
                    <div class="col-4">
                        <q-btn push class="bg-cyan-4 text-white" size="xl" label="Database" icon="storage" style="width:100%;height:10vh;" @click="handleChoice" />
                    </div>

                </div>
            </q-card-section>

        </div>
    </q-card>
</div>
</template>

<script lang="js">
import {
    axiosInstance
} from '@/api/axios';
import {
    defineComponent,
    ref
} from 'vue';

export default defineComponent({
    name: 'OptionsProivsionsView',
    emits: ["next", "back", "error"],
    watch: {
        file() {
            // this.$emit("choose", false, this.file)
            this.handleChoice(false)
        }
    },
    data() {
        return {
            label: ref("hello"),
            file: ref(null),
            usingDatabase: false,
        }
    },
    methods: {
        handleChoice(usingDatabase) {
            if (!usingDatabase) {
                if (this.file.type !== "text/csv") {
                    this.$emit('error', "The file provided is not a CSV file.")
                } else {
                    var formData = new FormData()
                    formData.append("data", this.file)
                    const payload = {
                        "data_using_csv": !this.usingDatabase,
                        "code": this.$route.params.room_id,
                    }
                    formData.append("payload", JSON.stringify(payload))
                    axiosInstance.post("api-generate/generator/validate-data-file/", formData, {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        }
                    }).then(
                        response => {
                            if (response.status == 200) {
                                this.$store.commit(
                                    "setDataProvision",
                                    usingDatabase,
                                    this.file
                                )
                                this.$emit("next")
                            } else {
                                this.$emit('error', response.data.detail)
                            }
                        }
                    )
                }
            } else {
                this.$store.commit(
                    "setDataProvision",
                    usingDatabase,
                    this.file
                ) 
                this.$emit("next")
            }
        }
    }
});
</script>
