<template>
  <div class="demo">
    <div class="title mt-3 text-center bold">
      Demo for Computer Vision project
    </div>
    <div class="upload-image mt-3 text-center">
      <input
        type="file"
        class="custom-file-input"
        accept="image/*"
        @change="uploadImage($event)"
        id="file-input"
      />
      <label class="file-label">Choose file</label>
      <div id="loading" class="spinner-border text-danger" role="status">
        <span class="sr-only">Loading...</span>
      </div>
    </div>

    <div class="container">
      <div class="row">
        <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6">
          <div
            v-if="rawImage !== null"
            class="text-label product-list mt-3 text-center"
          >
            Original image
            <div class="mt-3">
              <img :src="rawImage" />
            </div>
          </div>
        </div>
        <div class="col-xs-12 col-sm-12 col-md-6 col-lg-6">
          <div v-show="resultLink !== null" class="mt-3">
            <div class="text-label mt-3 text-center">Text result preview</div>
            <iframe
              id="txt-result"
              ref="txtResult"
              :src="resultLink"
              frameborder="0"
              width="100%"
              height="100%"
            ></iframe>
          </div>
        </div>
      </div>
    </div>
    <div class="container">
      <div
        v-if="textRegionImage !== null"
        class="text-label text-region mt-3 text-center"
      >
        Text region
        <div class="mt-3">
          <img :src="textRegionImage" />
        </div>
      </div>
    </div>
    <div v-if="listTextBoxImage.length > 0" class="container">
      <div class="text-label text-center">
        Text box
      </div>
      <div
        class="row text-box mt-3 text-center"
      >
        <div
          class="text-box-img mt-3 mr-3 col-xs-12 col-sm-6 col-md-3 col-lg-3"
          v-for="textBoxImg in listTextBoxImage"
          :key="textBoxImg.id"
        >
          <img :src="textBoxImg.src" />
        </div>
      </div>
    </div>
    <div v-if="resultLink !== null" class="download mt-3 text-center mb-5">
      <button class="btn btn-danger" @click="download">Download result</button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Demo",
  data() {
    this.DOWNLOAD_URL = "http://localhost:5000/download";

    return {
      rawImage: null,
      textRegionImage: null,
      finalResult: null,
      resultLink: null,
      listTextBoxImage: [],
    };
  },
  methods: {
    uploadImage(event) {
      const me = this;
      axios.defaults.headers.post["Content-Type"] =
        "application/json;charset=utf-8";
      axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
      const URL = "http://localhost:5000/upload";

      let data = new FormData();
      const file = event.target.files[0],
        fileExtension = file.name.split(".").pop();
      data.append("file_name", file.name);
      data.append("file", file);
      data.append("file_extension", fileExtension);

      let config = {
        header: {
          "Content-Type": `image/${fileExtension}`,
        },
      };

      me.mask();

      axios.post(URL, data, config).then((response) => {
        console.log("image upload response > ", response);
        const data = response.data;
        me.rawImage = data.raw_image;
        me.textRegionImage = data.text_region_image;
        me.listTextBoxImage = data.list_text_box_image;
        me.resultLink = me.DOWNLOAD_URL;

        setTimeout(function () {
          me.refreshIframe();
          me.unmask();
        }, 2000);
      });
    },
    /**
     * reload iframe
     */
    refreshIframe() {
      const iframe = document.getElementById("txt-result");
      // iframe.src = this.DOWNLOAD_URL;
      iframe.src = "http://localhost:5000/download";
    },
    download() {
      window.parent.caches.delete("call");
      window.open(this.DOWNLOAD_URL, "_blank");
    },
    mask() {
      const loading = document.getElementById("loading");
      loading.style.display = "inline-flex";
    },
    unmask() {
      const loading = document.getElementById("loading");
      loading.style.display = "none";
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
.text-label {
  font-size: 20px;
  font-weight: bold;
  color: cornflowerblue;
}
.upload-image {
  position: relative;
}
.text-box-img {
  border: 1px solid grey;
  padding: 1rem;
}
#txt-result {
  text-align: center;
  min-height: 500px;
}
#file-input {
  width: 171px;
  height: 60px;
  cursor: pointer;
  margin: auto auto;
  display: block;
}
.file-label {
  cursor: pointer;
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  z-index: 1;
  /* height: calc(1.5em + .75rem + 2px); */
  padding: 1rem 1.75rem;
  font-weight: 400;
  /* line-height: 1.5; */
  color: #495057;
  background-color: #fff;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  width: 170px;
  left: 50%;
  transform: translateX(-50%);
}
#loading {
  display: none;
  position: absolute;
  top: 14px;
  left: calc(50% - 20px);
  z-index: 2;
}
</style>
