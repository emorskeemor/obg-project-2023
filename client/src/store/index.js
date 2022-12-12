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
    blocks_must_align: false,
    class_size: 0,
    lesson_cost: 0,
    max_subjects_per_block: 0,
    settings_title: "",
    settings_id: 0,
    options_id: 0,
    // evluation details
  },
  getters: {
  },
  mutations: {
    setEvaluation(state, evaluation){
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
      state.blocks_must_align = data.settings.blocks_must_align
      state.classSize = data.settings.class_size
      state.lesson_cost = data.settings.lesson_cost
      state.max_subjects_per_block = data.settings.max_subjects_per_block
      state.settings_title = data.settings.title
      state.settings_id = data.settings.id
      state.options_id = data.opts_id
    }
  },
  actions: {
  },
  modules: {
  }
})
