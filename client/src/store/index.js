import { ref } from 'vue'
import { createStore } from 'vuex'

export default createStore({
  state: {
    // evaluation
    generated_blocks: [],
    successful_students: [],
    failed_students:[],
    // provision type
    using_database:false,
    data_file: ref(null),
    // settings data
    blocks: 0,
    blocksMustAlign: false,
    classSize: 0,
    lessonCost: 0,
    maxSubjectsPerBlock: 0,
    settingsTitle: "",
    settingsId: 0,
    optionsId: 0,
  },
  getters: {
  },
  mutations: {
    setEvaluation(state, evaluation){
      console.log(evaluation);
      state.generated_blocks = evaluation.blocks
      state.successful_students = evaluation.students.success
      state.failed_students = evaluation.students.failed
    },
    setDataProvision(state, usingDatabase, file){
      state.using_database = usingDatabase
      if (!usingDatabase){
        state.data_file = file
      }
    },
    setSettingsData(state, data) {
      state.blocks = data.settings.blocks;
      state.blocksMustAlign = data.settings.blocks_must_align
      state.classSize = data.settings.class_size
      state.lessonCost = data.settings.lesson_cost
      state.maxSubjectsPerBlock = data.settings.max_subjects_per_block
      state.settingsTitle = data.settings.title
      state.settingsId = data.settings.id
      state.optionsId = data.opts_id
    }
  },
  actions: {
  },
  modules: {
  }
})
