<script setup>
// No necesitamos importar nada porque ya no usamos store aquí
</script>

<template>
  <footer class="py-3 footer">
    <div class="container-fluid">
      <div class="row align-items-center justify-content-lg-between">
        <div class="mb-4 col-lg-6 mb-lg-0">
          <div class="text-sm text-center copyright text-muted text-lg-start">
            © {{ new Date().getFullYear() }}, desarrollado por
            <a
              href="#"
              class="font-weight-bold"
              target="_blank"
            >
              ORVIDA
            </a>
             - tecnología que conecta y transforma.
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>
