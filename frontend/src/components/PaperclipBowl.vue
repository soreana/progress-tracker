<!-- PaperclipBowl.vue (Vue 3 + Composition API) -->
<template>
  <BContainer class="row justify-content-center">
    <!-- Error Message Alert -->
    <div class="error-message" v-if="showError">
      <div class="alert alert-danger alert-dismissible fade show" role="alert">
        {{ errorMessage }}
        <button type="button" class="btn-close" @click="showError = false" aria-label="Close"></button>
      </div>
    </div>
    
    <BRow>
      <!-- Bowl A -->
      <BCol cols="4">
        <div class="bowl">
          <h2 class="text-center fw-bold">🎯 To be implemented</h2>
          <div class="bowl-area" @dragover.prevent @drop="(event) => dropClipTo('left', event)">
            <div 
                v-for="clip in leftClips"
                :key="clip.id"
                class="paperclip-container"
                draggable="true"
                @dragstart="(event) => dragStart(clip, 'left', event)"
            >
              <img
                  :src="'images/paperclip.png'"
                  alt=""
                  class="paperclip"
                  :style="{ width: clip.size + 'px', height: clip.size + 'px' }"
              />
              <div class="clip-name">{{ clip.name }}</div>
            </div>
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
            <div
                v-for="clip in rightClips"
                :key="clip.id"
                class="paperclip-container"
                draggable="true"
                @dragstart="(event) => dragStart(clip, 'right', event)"
            >
              <img
                  :src="'images/paperclip.png'"
                  alt=""
                  class="paperclip"
                  :style="{ width: clip.size + 'px', height: clip.size + 'px' }"
              />
              <div class="clip-name">{{ clip.name }}</div>
            </div>
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
// const baseURL = `${window.location.protocol}//${window.location.host}/api`;
const baseURL = 'http://127.0.0.1:5000';
const errorMessage = ref('');
const showError = ref(false);

// Collection of AML-themed unauthorized error messages
const unauthorizedMessages = [
  "🚨 SUSPICIOUS ACTIVITY REPORT: Unusual paperclip movement pattern detected. Transaction blocked pending enhanced due diligence.",
  
  "🔍 KYC VERIFICATION FAILED: Your identity hasn't been verified for this high-risk paperclip transaction. Please complete the customer due diligence process.",
  
  "⛔ SANCTIONS ALERT: This paperclip appears on the Office of Foreign Assets Control (OFAC) specially designated nationals list. Transfer blocked.",
  
  "🔐 COMPLIANCE BREACH: Attempted paperclip movement violates the Anti-Paperclip Laundering Act of 2023. This incident will be reported to FinCEN.",
  
  "⚠️ RISK RATING ELEVATED: Your paperclip risk score has exceeded threshold (999+). Please contact the compliance department for remediation.",
  
  "🧐 BENEFICIAL OWNERSHIP UNCLEAR: Cannot determine the ultimate beneficial owner of this paperclip. Transaction rejected per CDD Final Rule.",
  
  "📊 UNUSUAL TRANSACTION: This paperclip movement deviates from your established baseline activity pattern. Additional verification required.",
  
  "📝 MISSING DOCUMENTATION: Paperclip source of funds declaration required. Please submit origin of paperclip attestation form.",
  
  "🌐 JURISDICTIONAL CONTROL FAILURE: This paperclip movement crosses high-risk jurisdictions without proper AML controls. Transfer rejected.",
  
  "💼 REGULATORY COMPLIANCE NOTICE: Your PEP (Politically Exposed Paperclip) requires senior management approval before movement.",
  
  "🔒 BLOCKCHAIN COMPLIANCE ERROR: This paperclip's transaction history contains obfuscated hops through mixing services. Movement prohibited.",
  
  "📱 DIGITAL IDENTITY VERIFICATION FAILED: Your biometric paperclip manipulation credentials have been declined. Please try another authentication method.",
];

// Function to get a random unauthorized message
function getRandomUnauthorizedMessage() {
  const randomIndex = Math.floor(Math.random() * unauthorizedMessages.length);
  return unauthorizedMessages[randomIndex];
}

// Function to extract token from URL and store it
function extractAndStoreToken() {
  const urlParams = new URLSearchParams(window.location.search);
  const token = urlParams.get('token');
  
  if (token) {
    localStorage.setItem('paperclipAuthToken', token);
    // Clean URL by removing the token parameter
    const newUrl = window.location.pathname + window.location.hash;
    window.history.replaceState({}, document.title, newUrl);
  }
}

// Function to get the stored token
function getAuthToken() {
  return localStorage.getItem('paperclipAuthToken');
}

onMounted(async () => {
  // Extract and store token if present in URL
  extractAndStoreToken();
  
  try {
    const response = await axios.get(`${baseURL}/get_state`)
    generateClips(response.data.left, leftClips, 'L')
    generateClips(response.data.right, rightClips, 'R')
  } catch (error) {
    console.error("Failed to fetch initial state:", error);
    showErrorMessage("Failed to load paperclips. Please refresh the page.");
  }
})

// Function to display error messages
function showErrorMessage(message, duration = 5000) {
  errorMessage.value = message;
  showError.value = true;
  
  // Hide error message after duration
  setTimeout(() => {
    showError.value = false;
  }, duration);
}

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
    // Include the auth token in the request
    const token = getAuthToken();
    await axios.post(`${baseURL}/move_clip`, {
      id: clipId,
      direction,
      token: token
    });
    
    // If successful, update the UI
    const fromArray = sourceBowl === 'left' ? leftClips : rightClips
    const toArray = destination === 'right' ? rightClips : leftClips

    fromArray.value = fromArray.value.filter(c => c !== draggedClip)
    toArray.value.push({...draggedClip})
    
  } catch (e) {
    console.error("Failed to update backend:", e);
    
    // Handle unauthorized error
    if (e.response && (e.response.status === 401 || e.response.status === 403)) {
      showErrorMessage(getRandomUnauthorizedMessage());
    } else {
      showErrorMessage("Error moving paperclip: " + (e.response?.data?.message || "Something went wrong"));
    }
    return;
  } finally {
    draggedClip = null;
    sourceBowl = null;
  }
}
</script>

<style scoped>
.error-message {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  max-width: 80%;
  width: 500px;
}

.bowl {
  background: white;
  padding: 16px;
  border-radius: 16px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 500px;
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

.paperclip-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 6px;
  cursor: grab;
}

.clip-name {
  font-size: 12px;
  margin-top: 4px;
  text-align: center;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>

