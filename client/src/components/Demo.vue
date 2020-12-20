<template>
  <div class="demo">
    <div class="title mt-3 text-center bold">Demo for Computer Vision project</div>
    <div class="upload-image mt-3 text-center">
      <input
        type="file"
        accept="image/*"
        @change="uploadImage($event)"
        id="file-input"
      />
    </div>
    <div class="product-list mt-3 text-center">Product list</div>
    <div class="text-region mt-3 text-center">Text region</div>
    <div class="text-box mt-3 text-center">Text box</div>
    <div class="result mt-3 text-center">Text result</div>
    <div class="download mt-3 text-center">Download result</div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Demo",
  methods: {
    uploadImage(event) {
      const URL = "http://localhost:5000/demo";

      let data = new FormData();
      data.append("name", "demo");
      data.append("file", event.target.files[0]);

      let config = {
        header: {
          "Content-Type": "image/png",
        },
      };

      axios.put(URL, data, config).then((response) => {
        console.log("image upload response > ", response);
      });
    },
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
.mt-3 {
  margin-top: 3rem;
}
.bold {
  font-weight: bold;
}
.title {
  font-size: 30px;
}
</style>
