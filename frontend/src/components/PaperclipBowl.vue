<!-- PaperclipBowl.vue (Vue 3 + Composition API) -->
<template>
  <BContainer class="row justify-content-center">
    <BRow>
      <!-- Bowl A -->
      <BCol cols="4">
        <div class="bowl">
          <h2 class="text-center fw-bold">🎯 To be implemented</h2>
          <div class="bowl-area" @dragover.prevent @drop="(event) => dropClipTo('left', event)">
            <img
                v-for="clip in leftClips"
                :src="'images/paperclip.png'"
                alt=""
                :key="clip.id"
                class="paperclip"
                :style="{ width: clip.size + 'px', height: clip.size + 'px' }"
                draggable="true"
                @dragstart="(event) => dragStart(clip, 'left', event)"
            />
          </div>
        </div>
      </BCol>
      <BCol cols="4">

      </BCol>

      <!-- Bowl B -->
      <BCol cols="4">
        <div class="bowl">
          <h2 class="text-center fw-bold">🏆 Implemented</h2>
          <div class="bowl-area" @dragover.prevent @drop="(event) => dropClipTo('right', event)">
            <img
                v-for="clip in rightClips"
                :src="'images/paperclip.png'"
                :key="clip.id"
                class="paperclip"
                :style="{ width: clip.size + 'px', height: clip.size + 'px' }"
                draggable="true"
                @dragstart="(event) => dragStart(clip, 'right', event)"
                alt=""
            />
          </div>
        </div>
      </BCol>
    </BRow>
  </BContainer>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import axios from 'axios'
import {BContainer, BRow, BCol} from "bootstrap-vue-next";

const leftClips = ref([])
const rightClips = ref([])
let draggedClip = null
let sourceBowl = null

onMounted(async () => {
  const response = await axios.get('http://127.0.0.1:5000/get_state')
  generateClips(response.data.left, leftClips, 'L')
  generateClips(response.data.right, rightClips, 'R')
})

function generateClips(clips, targetClips) {
  function createClipObject(clip) {
    return {
      id: clip.id,
      name: clip.name,
      size: 10 + clip.size * 20,
    };
  }

  for (const clip of clips) {
    targetClips.value.push(createClipObject(clip));
  }
}

function dragStart(clip, from, event) {
  draggedClip = clip
  sourceBowl = from

  event.dataTransfer.setData('clipId', clip.id)
}

async function dropClipTo(destination, event) {
  const clipId = event.dataTransfer.getData('clipId')

  if (!draggedClip || sourceBowl === destination) return

  const direction = sourceBowl === 'left' ? 'left_to_right' : 'right_to_left'
  try {
    await axios.post('http://127.0.0.1:5000/move_clip', {id : clipId , direction})
  } catch (e) {
    console.error("Failed to update backend:", e)
    return
  }

  const fromArray = sourceBowl === 'left' ? leftClips : rightClips
  const toArray = destination === 'right' ? rightClips : leftClips

  fromArray.value = fromArray.value.filter(c => c !== draggedClip)
  toArray.value.push({...draggedClip})
  draggedClip = null
  sourceBowl = null
}
</script>

<style scoped>
.bowl {
  background: white;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 250px;
}

.bowl-area {
  min-height: 300px;
  background: #f0f0f0;
  border-radius: 8px;
  padding: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  justify-content: center;
  align-items: flex-end;
}

.paperclip {
  border-radius: 50%;
  cursor: grab;
}
</style>

