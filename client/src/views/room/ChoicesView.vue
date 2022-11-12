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
                :group="{name:'availableOptions', pull:'clone', put:false}"
                :clone="cloneOption"
                itemKey="title"
                :move="moveOption"
                id="availableOptions"
              >
              <!-- iterate over all available options in pagination -->
              <template #item="{element}">
                <div class="row justify-center items-center">
                  <q-card style="width:40vh;margin:1vh" class="bg-teal-3 glossy">
                    <q-card-section>
                      <div class="text-h5 text-white">{{element.title}}</div>
                    </q-card-section>
                    <!-- view info about the option -->
                    <q-card-actions>
                      <q-btn class="bg-blue text-white" @click="loadSubjectInfo(element)" icon="info" label="info">
                        
                      </q-btn>
                    </q-card-actions>
                  </q-card>
                </div>
              </template>
            </draggable>

            <!-- display a message to display if no searched pages are found -->
            <div v-if="getSearchedPages().length === 0">
              <q-card class="bg-grey-5 rounded-borders"  style="padding:5vh;margin:3vh">
                <div class="text-h4 text-black main-font">Whoopsie!</div>
                <div class="text-h6">We could not find the subject you are looking for.</div>
              </q-card>
            </div>

            <!-- display a skeleton if the options have not yet loaded -->
            <div v-if="fetching">
              <div  v-for="i in [1,2,3]" :key="i">
                <div class="row justify-center items-center">
                    <q-card style="width:40vh;margin:1vh" class="bg-teal-3 glossy">
                      <q-card-section>
                        <q-skeleton type="text" />
                      </q-card-section>
                      <q-separator dark inset />
                      <q-card-actions class="justify-center">
                        <q-skeleton type="QBtn" />

                      </q-card-actions>
                    </q-card>
                  </div>

              </div>
            </div>
            
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
                active-color="red-5"
                :modelValue="availableOptionsPage"
                :boundary-numbers="false"

              />
            </div>
            </q-card>
            
          </div>
          <!-- details about the option block choice -->

          <div class="col">
            <q-card class="bg-grey-3" style="padding:20px;min-height:75vh">
              <!-- details about how to choose the options -->
              <div class="text-h4 text-black main-font">Hello {{studentData.firstName}} {{studentData.lastName}}</div>

              <div class="text-body1">Drag the subjects you would like to take into the chosen subjects section to the right</div>

              <!-- display how may subjects the student can take -->
              <q-separator color="black" spaced/>
              <div class="text-h6 text-black main-font text-weight-medium">You are able to take {{maximumAllowedOptions}} subjects</div>
              <div class="text-h6 text-black main-font text-weight-medium">and {{maximumReserveOptions}} reserve options</div>

              <q-separator color="black" spaced/>
              <!-- reserve options -->
              <q-card-section class="block full-height">
                <draggable
                  class="list-group"
                  :list="reserveOptions"
                  :group="{name:'reserveOptions', pull:true, put:true}"
                  itemKey="name"
                  id="reserveOptions"
                  >
                    <template #item="{element, index}">
                      <div class="row justify-center items-center">
                        <q-card style="width:40vh;margin:1vh;max-height:15vh;" class="bg-teal-3 glossy">
                          <q-card-section style="padding:5px">
                            <div class="text-h5 text-white">{{element.title}}</div>
                          </q-card-section>
                          <q-separator dark inset />
                          <q-card-actions>
                            <q-btn class="bg-blue-grey text-white" @click="removeReserveOption(index)" icon="highlight_off" label="remove"/>
                        <q-btn class="bg-blue text-white" @click="loadSubjectInfo(element)" icon="info" label="info"/>
                          </q-card-actions>
                        </q-card>
                      </div>
                    </template>
                  </draggable>
                  <div v-if="reserveOptions.length == 0 && !fetching" class="bg-grey-5 rounded-borders" style="padding:10px">
                    <div class="text-h5 text-black main-font">Drag a reserve subject<div class="text-weight-bold">above</div> this box</div>
                  </div>
              </q-card-section>
              <!-- save options and reserves -->
              <div class="absolute-bottom justify-center bg-grey-4" style="padding:10px">
                <q-btn-group>
                  <q-btn class="bg-red-5 text-white" style="width:15vh" icon-right="check_circle" size="small" label="save"
                  :disable="chosenOptions.length != maximumAllowedOptions || reserveOptions.length !== maximumReserveOptions"
                  />
                  <q-btn class="bg-blue text-white" style="width:15vh" icon-right="help" size="small" label="help"/>
                </q-btn-group>
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
              :group="{name:'chosenOptions', pull:true, put:true}"
              itemKey="name"
              id="chosenOptions"
              >
                <template #item="{element, index}">
                  <div class="row justify-center items-center">
                    <q-card style="width:40vh;margin:1vh;max-height:15vh;" class="bg-teal-3 glossy">
                      <q-card-section style="padding:5px">
                        <div class="text-h5 text-white">{{element.title}}</div>
                        <q-badge color="red-12 row justify-center rounded-borders" floating rounded style="width:4vh;height:4vh">
                          <div class="text-h5 text-white">{{index+1}}</div>
                        </q-badge>
                      </q-card-section>
                      <q-separator dark inset />
                      <q-card-actions>
                        <q-btn class="bg-blue-grey text-white" @click="removeChosenOption(index)" icon="highlight_off" label="remove"/>
                        <q-btn class="bg-blue text-white" @click="loadSubjectInfo(element)" icon="info" label="info"/>
                      </q-card-actions>
                    </q-card>
                  </div>
                </template>
              </draggable>
            <!-- display a skeleton if the options have not yet loaded -->
            <div v-if="fetching">
              <div  v-for="i in [1,2,3,4]" :key="i">
                <div class="row justify-center items-center">
                    <q-card style="width:40vh;margin:1vh" class="bg-teal-3 glossy">
                      <q-card-section>
                        <q-skeleton type="text" />
                      </q-card-section>
                      <q-separator dark inset />
                      <q-card-actions class="justify-center">
                        <q-skeleton type="QBtn" />
                      </q-card-actions>
                    </q-card>
                  </div>
              </div>
            </div>
            <!-- display a box to indicate where to place the subject -->
            <div v-if="chosenOptions.length == 0 && !fetching">
              <q-card class="bg-grey-5 rounded-borders"  style="padding:1vh;margin-inline:3vh;margin-top: 10px;">
                <div class="text-h5 text-black main-font">Drag in an option <div class="text-weight-bold">above</div> this box</div>
              </q-card>
            </div>
            <div class="row justify-center bg-grey-4 absolute-bottom" style="padding:1vh">

            </div>
            </q-card>
          </div>
        </div>
        <!-- banner to show any errors raised when moving options -->
        <q-banner inline-actions class="text-white bg-red absolute-bottom" v-if="this.errorMessage.length !== 0">
        <div class="absolute-center">
          {{errorMessage}}
        </div>
        <template v-slot:action>
          <q-btn flat color="white" label="Dissmis" @click="this.errorMessage=''" />
        </template>
      </q-banner>

      <q-dialog v-model="displaySubjectInfo">
        <q-card>
          <q-card-section class="bg-teal-3 glossy">
            <div class="text-h6 text-white text-weight-bold">{{displaySubjectDetails.title}},{{displaySubjectDetails.subject_code}}</div>
          </q-card-section>

          <q-card-section class="q-pt-none q-pa-sm">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt 
            ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco 
            laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit 
            in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat 
            cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          </q-card-section>

          <q-card-actions align="right">
            <q-btn flat label="OK" color="primary" v-close-popup />
          </q-card-actions>
        </q-card>
      </q-dialog>
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
      reserveOptions:[],
      // CHANGE LATER FROM REQUEST
      maximumReserveOptions:2,
      maximumAllowedOptions:0,
      
      availableOptions:[],
      availableOptionsPage:1,
      availableOptionsCount:0,
      maximumOptionPages:0,

      fetching:true,
      // student data
      studentData: {
        firstName:"",
        lastName:"",
        uuid:""
      },
      search:"",
      displaySubjectInfo:false,
      displaySubjectDetails: {},
      //
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
            this.maximumAllowedOptions = data.max_choices
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
  beforeRouteLeave (to, from , next) {
    const answer = window.confirm('Do you really want to leave? you have unsaved changes!')
    if (answer) {
      next()
    } else {
      next(false)
    }
  },
  methods:{
    moveOption(event) {
      // validate reseve options
      this.errorMessage = ""
      if (event.to.id == "reserveOptions") {
        if (this.reserveOptions.length >= this.maximumReserveOptions){
          this.errorMessage = "Too many reserve options"
          return false
        } else {
          for (let i=0; i < this.reserveOptions.length; i++){
            if (event.draggedContext.element.uuid === this.reserveOptions[i].uuid){
              this.errorMessage = "You have already chosen this subject as a reserve option"
              return false
            }
          }
          for (let i=0; i < this.chosenOptions.length; i++){
            if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid){
              console.log("no thanks");
              this.errorMessage = "This subject has already been used as a main option"
              return false
            }
          }
        }
      // validate chosen options
      } else if (event.to.id == "chosenOptions"){
        if (this.chosenOptions.length >= this.maximumAllowedOptions){
          this.errorMessage = "Too many options"
          return false
        } else {
          for (let i=0; i < this.reserveOptions.length; i++){
            if (event.draggedContext.element.uuid === this.reserveOptions[i].uuid){
              this.errorMessage = "You have already chosen this subject as a reserve option"
              return false
            }
          }
          for (let i=0; i < this.chosenOptions.length; i++){
            if (event.draggedContext.element.uuid === this.chosenOptions[i].uuid){
              this.errorMessage = "This subject has already been chosen"
              return false
            }
          }
        }
      }
    },
    cloneOption(option){
      return option
    },
    removeChosenOption(index){
      this.errorMessage = ""
      this.chosenOptions.splice(index, 1)
    },
    removeReserveOption(index){
      this.errorMessage = ""
      this.reserveOptions.splice(index, 1)
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
    loadSubjectInfo(subject){
      this.displaySubjectInfo = true
      this.displaySubjectDetails = subject
    },
    closeSubjectInfo(){
      this.displaySubjectInfo = false
    }

  }
  
});
</script>

