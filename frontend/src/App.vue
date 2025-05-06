<script setup>
import PaperclipBowl from './components/PaperclipBowl.vue'
</script>

<template>
  <div>
    <a href="https://jamesclear.com/paper-clips" target="_blank" rel="noopener noreferrer" class="reference-link">
      📎 Learn about the Paper Clips Strategy
    </a>
    <PaperclipBowl />
  </div>
</template>

<style scoped>
.reference-link {
  position: fixed;
  top: 25px;
  right: 25px;
  background-color: #f8f9fa;
  color: #007bff;
  padding: 8px 12px;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 500;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.2s ease;
  z-index: 1000;
  font-size: 16px;
}

.reference-link:hover {
  background-color: #e9ecef;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
</style>
