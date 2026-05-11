<script setup>
defineProps({
  currentPage: {
    type: String,
    required: true,
  },
  color: {
    type: String,
    default: "text-dark",
  },
});
</script>

<template>
  <nav aria-label="breadcrumb">
    <ol class="px-0 pt-1 pb-0 mb-0 bg-transparent breadcrumb me-sm-6">
      <li class="text-sm breadcrumb-item" :class="color">
        <a class="opacity-8" :class="color" href="#">Pages</a>
      </li>
      <li
        class="text-sm breadcrumb-item active"
        :class="color"
        aria-current="page"
      >
        {{ currentPage }}
      </li>
    </ol>
    <h6 class="mb-0 font-weight-bolder" :class="color">
      {{ currentPage }}
    </h6>
  </nav>
</template>
