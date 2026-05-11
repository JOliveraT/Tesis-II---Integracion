<script setup>
import { ref, watch, nextTick } from 'vue';
import { gsap } from 'gsap';
const props = defineProps({ winnerName: String, stateLabel: String });
const titleRef = ref();
watch(() => props.winnerName, async (v) => { if (!v) return; await nextTick(); gsap.fromTo(titleRef.value,{scale:0.5,opacity:0},{scale:1.2,opacity:1,duration:1,yoyo:true,repeat:1}); });
</script>
<template><div class='card anim'><h3 ref='titleRef'>{{ winnerName || 'Esperando resultado del backend...' }}</h3><p>{{ stateLabel }}</p></div></template>
