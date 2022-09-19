<template>
    <q-page class="q-pa-xl absolute-center" padding >
      <h1 style="font-family:'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
        class="text-h1" >
        Join a room
      </h1>
      <div style="width:500px" >
        <q-input
            filled
            v-model="domainName"
            label="Domain *"
            hint="domain"
            lazy-rules
            type="text"
            :rules="[val => !!val || '* Required',]"
        >
        <template v-slot:prepend>
            <q-icon name="domain"/>
        </template>
        </q-input>
        <q-input
            filled
            v-model="roomCode"
            label="Room code *"
            hint="roomcode"
            lazy-rules
            type="text"
            :rules="[
            val => !!val || '* Required',
            val => val.length === 8 || 'A code is 8 characters long',
        ]"
        >
        <template v-slot:prepend>
            <q-icon name="home"/>
        </template>
        </q-input>
        <q-btn class="bg-green-13 text-white" push size="20px">
            Join
        </q-btn>

      </div>
      
    </q-page>
</template>

<script lang="ts">
import { defineComponent } from 'vue';


export default defineComponent({
  name: 'RoomJoinView',
  data(){
    return {
        roomCode: "",
        domainName: ""
    }
  },
  methods:{

  }
});
</script>
