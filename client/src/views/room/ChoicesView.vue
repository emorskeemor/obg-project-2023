<template>
    <q-page class="q-pa-xs no-scroll" padding >
        <div class="row q-gutter-xl q-pa-md">

          <!-- available options that the student can choose from -->
          <div class="col-4 q-gutter-md">
            <q-card class="bg-grey-3" style="min-height:77vh">
              <q-card-section class="bg-grey-4">
                <div class="text-h4 text-black main-font" style="padding-bottom:1vh">Available options</div>
                <q-input
                    filled
                    v-model="search"
                    label="Search"
                    lazy-rules
                    type="text"
                    >
                  <template v-slot:prepend>
                      <q-icon name="search"/>
                  </template>
                </q-input>
              </q-card-section>
              <draggable
              v-if="!fetching"
              class="list-group"
              :list="getSearchedPages()"
              :group="{name:'available_options', pull:'clone', put:false}"
              :clone="cloneOption"
              itemKey="title"
              :move="moveOption">
              <!-- iterate over all available options in pagination -->
              <template #item="{element}">
                <div class="row justify-center items-center">
                  <q-card style="width:40vh;margin:1vh" class="bg-teal-3 glossy">
                    <q-card-section>
                      <div class="text-h5 text-white">{{element.title}}</div>
                    </q-card-section>
                    <q-separator dark inset />
                    <!-- view info about the option -->
                    <q-card-actions class="justify-center">
                      <q-btn class="bg-blue text-white" style="width:10vh">Info</q-btn>
                    </q-card-actions>
                  </q-card>
                </div>
              </template>
            </draggable>
            
            <!-- pagination  -->
            <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">
              <q-pagination
                v-model="availableOptionsPage"
                :max=maximumOptionPages
                :max-pages=5
                direction-links
                push
                color="teal"
                active-design="push"
                active-color="orange"
                :modelValue="availableOptionsPage"
                :boundary-numbers="false"

              />
            </div>
            </q-card>
            
          </div>
          <!-- details about the option block choice -->

          <div class="col">
            <q-card class="bg-grey-3" style="padding:20px;min-height:75vh">
              <div class="text-h4 text-black main-font">Details</div>
              <div class="text-body1">Drag the subjects you would like to take into the chosen subjects section to the right</div>
              <div class="absolute-bottom justify-center bg-grey-4" style="padding:10px">
                <q-btn class="bg-teal-13 text-white" style="width:10vh">Save</q-btn>
              </div>
            </q-card>
          </div>

          <!-- The chosen options the student has chosen -->
          <div class="col-4 q-gutter-md">
            
            <q-card class="bg-grey-3" style="min-height:77vh">
              
              <q-card-section class="bg-grey-4">
                <div class="text-h4 text-black main-font">Chosen options</div>
              </q-card-section>
              <draggable
              class="list-group"
              :list="chosenOptions"
              :group="{name:'chosen_options', pull:true, put:true}"
              itemKey="name"
            >
            <template #item="{element, index}">
              <div class="row justify-center items-center">
                <q-card style="width:40vh;margin:1vh;max-height:15vh;" class="bg-teal-3 glossy">
                  <q-card-section style="padding:5px">
                    <div class="text-h5 text-white">{{element.title}}</div>
                  </q-card-section>
                  <q-separator dark inset />
                  
                  <q-card-actions>
                    <q-btn class="bg-blue-grey text-white" style="width:10vh" @click="deleteChosenOption(index)">Delete</q-btn>
                    <q-btn class="bg-blue text-white" style="width:10vh">Info</q-btn>
                  </q-card-actions>
  
                </q-card>

              </div>
            </template>
            </draggable>
            <div v-if="chosenOptions.length == 0" class="bg-grey-5" style="padding:10px">
              <div class="text-h5 text-black main-font text-weight-medium">Drag in a subject here</div>
            </div>
            </q-card>
          </div>
        </div>
        <q-banner inline-actions class="text-white bg-red absolute-bottom" v-if="errorRaised">
        <div class="absolute-center">
          {{errorMessage}}
        </div>
        <template v-slot:action>
          <q-btn flat color="white" label="Dissmis" @click="errorRaised=false" />
        </template>
      </q-banner>
    </q-page>
</template>

<script lang="js">
import { axiosInstance } from '@/api/axios';
import { defineComponent } from 'vue';
import draggable from "vuedraggable";

const optionsPerPage = 3

export default defineComponent({
  name: 'StudentChoices',
  components: {
    draggable
  },
  display: "Custom Clone",
  order: 3,
  data() {
    return {
      // options the student has chosen
      chosenOptions:[],
      numberOfAllowedOptions:0,
      // available options to the user
      availableOptionsPage:1,
      availableOptionsCount:0,
      availableOptions:[],
      maximumOptionPages:0,
      fetching:true,
      // student data
      studentData: {
        firstName:"",
        lastName:"",
        uuid:""
      },
      search:"",
      //
      errorRaised:false,
      errorMessage:""
    }
  },
 
  beforeMount(){
    // we need to fetch some information before the data is rendered
    const params = this.$route.params
    this.fetching = true
    // get the student
    axiosInstance.get(
      `api-students/students/${params.id}`
      ).then(
        response=>{
          if (response.status == "200"){
            // student was found and we can get their current options
            // if any and their allowed number of choices
            const data = response.data
            this.chosenOptions = [...data.options]
            this.numberOfAllowedOptions = data.max_choices
            this.studentData.firstName = data.first_name
            this.studentData.lastName = data.last_name
            this.studentData.uuid = data.uuid
          } else if (response.status == "404") {
            // a 404 means the student uuid in the url was invalid
            // and we should redirect to a 404
            this.$router.push({name:"E404"})
          }

        }
      )
    // get the available options for the student
    axiosInstance.get(
      `api-rooms/available-option-choices/room-choices/?domain=${params.domain}&code=${params.code}&page=${this.availableOptionsPage}`
      ).then(response=>{
        this.availableOptions = response.data
        this.availableOptionsCount = this.availableOptions.length
        this.maximumOptionPages = Math.floor(this.availableOptionsCount/optionsPerPage) + 1
        this.fetching = false

      })
  },
  methods:{
    // option related methods
    moveOption(event) {
      // called whenever an options is moved
      this.errorRaised = false
      if (this.chosenOptions.length >= this.numberOfAllowedOptions){
        this.errorRaised = true
        this.errorMessage = "Too many options"
        return false
      } else {
        for (let i=0; i < this.chosenOptions.length; i++){
          if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid){
            console.log("no thanks");
            this.errorRaised = true
            this.errorMessage = "This subject has already been chosen"
            return false
          }
        }
      }
    },
    cloneOption(option){
      return option
    },
    deleteChosenOption(index){
      this.chosenOptions.splice(index, 1)
    },
    // searching and pagination
    searchFilter(option) {
      return (option.title.toLowerCase().includes(this.search))
    },
    getSearchedPages() {
      if (this.fetching) {
        return []
      }
      if (this.search === "") {
        return this.calculatePagination(this.availableOptions)
      } else {
        return this.calculatePagination(
          this.availableOptions.filter(this.searchFilter)
          );
      }
    },
    calculatePagination(options) {
      let startingPage = (this.availableOptionsPage-1)*optionsPerPage
      
      this.availableOptionsCount = options.length
      this.maximumOptionPages = Math.floor(this.availableOptionsCount/optionsPerPage) + 1

      return options.slice(
        startingPage,
        startingPage + optionsPerPage
      )

    },

  }
  
});
</script>

// http://localhost:8080/room/edgbarrow/GVQGUS90/s/0ae9ea0b-8405-4888-a43b-362e14156f41