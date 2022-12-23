<template>
<div style="min-height:70vh">
    <q-card class="absolute-center bg-grey-3 no-margin full-width full-height" square>
        <div class="row">
            <div class="col-8">
                <q-card square style="height:80vh">
                    <div class="row">
                        <div v-for="(i, index) in blocks" :key="i[0]" class="col q-pa-sm bg-grey-3">
                            <div class="text-h5 q-ma-sm">Option Block <div class="text-bold">[{{index+1}}] {{blocks[index].length}}</div>
                            </div>
                            <q-scroll-area style="height:60vh">
                                <draggable class="list-group" :list="blocks[index]" :id=index item-key="id" :group="{ name: 'people', pull: true, put: true }" :move="moveSubject" @start="startMove" @change="changeSubject" @end="finishedMove">
                                    <!-- iterate over all available options in pagination -->
                                    <template #item="{element}">
                                        <div :id="element">
                                            <q-card :class="current == element ? 'bg-red-6 q-pa-sm' : 'bg-grey-4 q-pa-sm'" @click="current=element" square>
                                                <div class="row">

                                                    <div class="col-2">
                                                        <div class="text-bold">{{element}}</div>
                                                    </div>
                                                    <div class="col-7">
                                                        {{this.$store.state.options[element]}}
                                                    </div>
                                                </div>
                                            </q-card>
                                        </div>
                                    </template>
                                </draggable>
                            </q-scroll-area>
                        </div>
                        <div class="col q-ma-md">
                            <div class="text-h4">Extra</div>
                            <div class="q-pa-md">
                                <div>Drag in extra subjects if required</div>
                            </div>
                            <q-scroll-area style="height:40vh">
                                <draggable class="list-group" item-key="id" :list="Object.keys(this.$store.state.options)" :group="{ name: 'people', pull: 'clone', put: false }" :move="moveSubject" @start="startMove" @change="changeSubject" @end="addSubject">
                                    <template #item="{element}">
                                        <div :id="element">
                                            <q-card :class="current == element ? 'bg-blue-5 q-pa-sm text-white text-bold' : 'bg-grey-3 q-pa-sm'" @click="current=element">
                                                {{element}}, {{this.$store.state.options[element]}}
                                            </q-card>
                                        </div>
                                    </template>
                                </draggable>
                            </q-scroll-area>
                            <div class="bg-grey-6 q-mt-md">
                                <div class="text-h6 text-white">
                                    <q-btn flat icon="delete" class="text-white" />
                                </div>
                                <draggable class="list-group" item-key="id" :list="[]" :group="{ name: 'trash', pull: false, put: true }" id="trash">
                                    <template #item="{element}">
                                        <div id="trash">
                                            <q-card class="bg-grey-6 q-pa-sm" square>
                                                {{element}}
                                            </q-card>
                                        </div>
                                    </template>
                                </draggable>
                                <div class="text-body1 text-white q-pa-sm">
                                    drag subjects above to delete them
                                </div>
                            </div>
                        </div>

                    </div>
                </q-card>
            </div>
            <div class="col-4">
                <q-card square style="height:80vh">
                    <q-card-section>
                        <div class="text-h3">statistics</div>
                    </q-card-section>
                    <q-card-section>
                        <div class="row">
                            <div class="text-body1">Success percentage : {{ this.$store.state.success_percentage }}</div>
                        </div>
                        <div class="row">
                            <div class="text-body1">Total subjects in blocks: {{totalSubjects}}</div>
                        </div>
                        <div class="row">
                            <div class="text-body1">generation time : {{ this.$store.state.debug_data.generation_time }}</div>
                        </div>
                        <div class="row">
                            <div class="text-body1">completed nodes : {{this.$store.state.debug_data.completed_nodes}}</div>
                        </div>
                        <div class="row">
                            <div class="text-body1">generated nodes: {{this.$store.state.debug_data.generated_nodes}}</div>
                        </div>
                        <div class="row">
                            <div class="text-body1">generated states: {{this.$store.state.debug_data.generated_states}}</div>
                        </div>
                    </q-card-section>
                    <q-separator />

                    <q-card-section>
                        <div class="row">
                            <div class="col">
                                <div class="text-h4 q-ma-sm">
                                    Operations
                                </div>
                                <div class="row bg-grey-3 justify-center">
                                    <div class="col-1 q-pa-sm text-bold justify-center items-center bg-grey-4">
                                        ID
                                    </div>
                                    <div class="col-2 q-pa-sm text-bold justify-center items-center bg-grey-5">
                                        Type
                                    </div>
                                    <div class="col-5 q-pa-sm text-bold justify-center items-center">
                                        Details
                                    </div>
                                    <div class="col q-pa-sm text-bold justify-center items-center">

                                    </div>
                                </div>
                                <q-separator />
                                <q-scroll-area style="height:25vh">
                                    <div v-if="operations.length !== 0">
                                        <div v-for="(op, index) in operations" :key="index">
                                            <q-card class="bg-grey-3" square>
                                                <div class="row justify-center items-center">
                                                    <div class="col-1 justify-center items-center q-pa-sm">
                                                        {{op.id}}
                                                    </div>
                                                    <div class="col-2 justify-center items-center">
                                                        {{op.type}}
                                                    </div>
                                                    <div class="col-5 justify-center items-center">
                                                        <div v-if="op.type==='MOVE'">
                                                            <div class="text-body1 text-center">Moving '{{op.subject}}' Block [{{op.target+1}}] to [{{op.to+1}}]</div>

                                                        </div>
                                                        <div v-else-if="op.type==='ADD'">
                                                            <div class="text-body1 text-center">Adding '{{op.subject}}' to Block [{{op.block+1}}]</div>

                                                        </div>
                                                        <div v-else-if="op.type==='REMOVE'">
                                                            <div class="text-body1 text-center">Removing '{{op.subject}}' from Block [{{op.block+1}}]</div>

                                                        </div>

                                                    </div>
                                                    <div class="col justify-center items-center">
                                                        <q-btn-group>
                                                            <q-btn flat class="bg-red-6 text-white" size="sm" label="delete" @click="removeOperation(op)" />
                                                            <q-btn flat class="bg-blue-6 text-white" size="sm" label="undo" @click="undoOperation(op)" />

                                                        </q-btn-group>
                                                    </div>
                                                </div>
                                            </q-card>
                                        </div>
                                    </div>
                                    <div v-else>
                                        <q-card class="q-pa-sm bg-grey-3" square>
                                            <div class="text-body1">
                                                Changes to the option blocks will show up here
                                            </div>
                                        </q-card>
                                    </div>
                                </q-scroll-area>

                            </div>
                        </div>
                    </q-card-section>
                    <q-separator />
                    <q-card-actions>
                        <q-btn-group>
                            
                        </q-btn-group>
                    </q-card-actions>
                </q-card>
            </div>
        </div>

    </q-card>
    <div class="absolute-bottom-right q-pa-md">
        <q-btn-group>
            <q-btn push class="bg-teal-4 text-white" size="md" label="evaluate" @click="evaluate" />
                            <q-btn push class="bg-red-6 text-white" size="md" label="reset" @click="reset" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="back" icon="undo" @click="$emit('back')" />
            <q-btn push class="bg-teal-4 text-white" size="md" label="next" icon="redo" @click="$emit('next')" />
        </q-btn-group>
    </div>

    <BannerComponent colour="red" @dismiss="dismissError" v-if="errorMessage" :message="errorMessage" />

</div>
</template>

<script lang="js">
import draggable from "vuedraggable";

import {
    defineComponent,
    ref
} from 'vue';
import {
    axiosInstance
} from "@/api/axios";
import BannerComponent from "../misc/BannerComponent.vue";

export default defineComponent({
    name: 'PreStatisticsView',
    emits: ["back", "next", "error", "dismissError"],
    components: {
        draggable,
        BannerComponent
    },
    data() {
        return {
            blocks: this.$store.state.generated_blocks.map(function (arr) {
                return arr.slice();
            }),
            current: "",
            operations: [],
            errorMessage: "",
        }
    },
    computed: {
        totalSubjects() {
            var count = 0
            this.blocks.forEach(item => {
                count = count + item.length
            })
            return count
        }
    },
    methods: {
        moveSubject(event, og) {
            if (event.relatedContext.list.includes(event.draggedContext.element) && event.from !== event.to) {
                this.errorMessage = `'${event.draggedContext.element}' already exists in this block`
                return false
            }
        },
        changeSubject(event) {
            // console.log(event);
        },
        startMove(arg) {
            this.$emit("dismissError")

            this.current = arg.item.id
        },
        finishedMove(event) {
            if (event.to !== event.from) {
                if (event.to.id === 'trash') {
                    this.operations.push({
                        id: this.operations.length + 1,
                        type: "REMOVE",
                        block: Number(event.from.id),
                        subject: event.clone.id,
                    })
                } else {

                    this.operations.push({
                        id: this.operations.length + 1,
                        type: "MOVE",
                        target: Number(event.from.id),
                        subject: event.clone.id,
                        to: Number(event.to.id)
                    })
                }
            }
        },
        addSubject(event) {
            if (event.to !== event.from) {
                this.operations.push({
                    id: this.operations.length + 1,
                    type: "ADD",
                    subject: event.item.id,
                    block: Number(event.to.id)
                })
            }
        },
        removeOperation(operation) {
            this.operations = this.operations.filter(op => op.id !== operation.id)
        },
        undoOperation(operation) {
            let type = operation.type
            let success = false
            // undo add operation by doing a remove operation
            if (type === "ADD") {
                let newBlocks = []
                let found = false
                this.blocks.forEach((block, index) => {
                    if (index == operation.block) {
                        newBlocks.push(block.filter(subject => {
                            if (subject === operation.subject && found === false) {
                                found = true
                            }
                            console.log(found);
                            return subject !== operation.subject
                        }))
                    } else {
                        newBlocks.push(block)
                    }
                })
                if (found === false) {
                    this.errorMessage = "Could not undo [ADD] operation as the subject no longer exists in the block"
                } else {

                    this.blocks = newBlocks
                    success = true
                }
                // undo a REMOVE operation by doing an add operation
            } else if (type === "REMOVE") {
                let found = false
                this.blocks[operation.block].forEach(
                    subject => {
                        if (subject === operation.subject) {
                            found = true
                        }
                    }
                )
                if (found === true) {
                    this.errorMessage = "Could not undo [REMOVE] operation as the subject already exists within this block"
                } else {
                    this.blocks[operation.block].push(operation.subject)
                    success = true
                }
            }
            // undo MOVE operation by reversing the move
            else if (type === "MOVE") {
                console.log(operation);
                if (this.subjectInBlock(operation.target, operation.subject)) {
                    this.errorMessage = `Cannot undo [MOVE] operation as '${operation.subject}' already exists in the original block [${operation.target+1}]`
                } else {
                    let found = false
                    let newBlocks = []
                    this.blocks.forEach((block, index) => {
                        // pop from the current block
                        if (index == operation.to) {
                            newBlocks.push(block.filter(subject => {
                                if (subject === operation.subject && found === false) {
                                    found = true
                                }
                                return subject !== operation.subject
                            }))
                            // add to the original block
                        } else if (index == operation.target) {
                            block.push(operation.subject)
                            newBlocks.push(block)
                        } else {
                            newBlocks.push(block)
                        }
                    })
                    console.log(newBlocks);
                    if (found === false) {
                        this.errorMessage = "Could not undo [ADD] operation as the subject no longer exists in the block"
                    } else {
                        this.blocks = newBlocks
                        success = true
                    }
                }
            }

            if (success === true) {

                this.removeOperation(operation)
            }

        },
        dismissError() {
            this.errorMessage = ""
        },
        reset() {
            this.blocks = this.$store.state.generated_blocks.map(function (arr) {
                    return arr.slice();
                }),
                this.current = ""
            this.operations = []
            this.dismissError()
        },
        evaluate() {
            axiosInstance.post("api-generate/generator/evaluate/", {
                initial: this.$store.state.generated_blocks,
                all_students: this.$store.state.all_students,
                new: this.blocks,
                operations: this.operations,
            }).then(response => {
                console.log(response);
            })
        },
        subjectInBlock(block, target) {
            let found = false
            this.blocks[block].forEach(
                subject => {
                    console.log(subject);
                    if (subject == target) {
                        found = true
                    }
                })
            return found
        }
    },

});
</script>
