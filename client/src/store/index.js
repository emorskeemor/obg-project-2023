import { ref } from 'vue'
import { createStore } from 'vuex'

export default createStore({
  state: {
    // evaluation
    generated_blocks: [],
    initial_blocks: [],
    successful_students: [],
    failed_students:[],
    all_students:[],
    success_percentage:0,
    debug_data: {},
    rules_followed: true,
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
    total_cost:0, 

    blocks_meta: {},
    // evluation details

    // subjects
    subjects:[],
    options:{},

    colours: ["bg-red", "bg-orange", "bg-yellow", "bg-green", "bg-light-blue"]
  },
  getters: {
  },
  mutations: {
    setEvaluation(state, evaluation){
      state.generated_blocks = evaluation.blocks
      state.successful_students = evaluation.students.success
      state.failed_students = evaluation.students.failed
      state.all_students = evaluation.all
      state.rules_followed = evaluation.rules_followed
      state.total_cost = evaluation.cost
      state.initial_blocks = state.generated_blocks.map(function (arr) {
        return arr.slice();
    })
      state.debug_data = evaluation.debug
      state.success_percentage = evaluation.success
      state.blocks_meta = evaluation.blocks_meta
    },
    setDataProvision(state, data){
      state.using_database = data.usingDatabase
      if (!data.usingDatabase){
        state.data_file = data.file
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
    },
    setPreStatistics(state, data){
      state.subjects = data.subjects
      state.options = data.options
    }
  },
  actions: {
  },
  modules: {
  }
})
