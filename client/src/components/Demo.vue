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
    <div class="product-list mt-3 text-center">
      Product list
      <div>
        <img :src="finalResult" >
      </div>
    </div>
    <div class="text-region mt-3 text-center">
      Text region
      <div>
        <img :src="finalResult" >
      </div>
    </div>
    <div class="text-box mt-3 text-center">
      Text box
      <div>
        <img :src="finalResult" >
      </div>
    </div>
    <div class="result mt-3 text-center">
      Text result
      <div>
        <img :src="finalResult" >
      </div>
    </div>
    <div class="download mt-3 text-center">
      <button @click="download">
        Download result
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "Demo",
  data() {
    return {
      finalResult: null
    }
  },
  methods: {
    uploadImage(event) {
      const me = this;
      axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
      axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
      const URL = "http://localhost:5000/upload";

      let data = new FormData();
      const file = event.target.files[0],
        fileExtension = file.name.split('.').pop();
      data.append("file_name", file.name);
      data.append("file", file);
      data.append("file_extension", fileExtension);

      let config = {
        header: {
          "Content-Type": `image/${fileExtension}`,
        },
      };

      axios.post(URL, data, config).then((response) => {
        console.log("image upload response > ", response);
        const data = response.data;
        me.finalResult = data.result_image;
      });
    },
    download() {
      const URL = 'http://localhost:5000/download';
      // axios.defaults.headers.post['Content-Type'] ='application/json;charset=utf-8';
      // axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
      // axios.get(URL).then((response) => {
      //   console.log("download response > ", response);
      //   // const data = response.data;
      // });
      window.parent.caches.delete("call")
      window.open(URL, '_blank');
    }
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
