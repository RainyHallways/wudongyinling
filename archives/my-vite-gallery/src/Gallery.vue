<template>
  <div class="gallery">
    <h1>Pixabay 图片画廊</h1>
    
    <div class="search">
      <input 
        v-model="searchQuery" 
        @keyup.enter="searchImages" 
        placeholder="搜索图片..."
      />
      <button @click="searchImages">搜索</button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    
    <div v-else class="image-grid">
      <div 
        v-for="(image, index) in images" 
        :key="image.id" 
        class="image-item"
        @click="openModal(index)"
      >
        <img 
          :src="image.webformatURL" 
          :alt="image.tags" 
          loading="lazy"
        />
        <div class="image-info">
          <span>👁️ {{ image.views }}</span>
          <span>❤️ {{ image.likes }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="showModal" class="modal" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-btn" @click="closeModal">&times;</button>
        <img :src="currentImage.largeImageURL" :alt="currentImage.tags" />
        <div class="modal-info">
          <p>摄影师: {{ currentImage.user }}</p>
          <p>标签: {{ currentImage.tags }}</p>
          <p>尺寸: {{ currentImage.imageWidth }} × {{ currentImage.imageHeight }}</p>
          <a :href="currentImage.pageURL" target="_blank" class="download-btn">
            在 Pixabay 上查看
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      images: [],
      loading: false,
      searchQuery: 'nature',
      showModal: false,
      currentImageIndex: 0,
      apiKey: '44071720-3b1b4d1a5a4e9c1b0d9f8e0d3' // 这是一个示例key，实际使用时请替换
    }
  },
  computed: {
    currentImage() {
      return this.images[this.currentImageIndex] || {}
    }
  },
  mounted() {
    this.fetchImages()
  },
  methods: {
    async fetchImages() {
      this.loading = true
      try {
        const response = await fetch(
          `https://pixabay.com/api/?key=${this.apiKey}&q=${this.searchQuery}&image_type=photo&per_page=20`
        )
        const data = await response.json()
        this.images = data.hits
      } catch (error) {
        console.error('获取图片失败:', error)
      } finally {
        this.loading = false
      }
    },
    searchImages() {
      if (this.searchQuery.trim()) {
        this.fetchImages()
      }
    },
    openModal(index) {
      this.currentImageIndex = index
      this.showModal = true
      document.body.style.overflow = 'hidden'
    },
    closeModal() {
      this.showModal = false
      document.body.style.overflow = ''
    }
  }
}
</script>

<style scoped>
.gallery {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.search {
  display: flex;
  justify-content: center;
  margin-bottom: 30px;
}

.search input {
  padding: 10px 15px;
  width: 300px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
}

.search button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 16px;
}

.search button:hover {
  background-color: #45a049;
}

.loading {
  text-align: center;
  padding: 50px;
  font-size: 18px;
}

.image-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.image-item {
  position: relative;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s;
}

.image-item:hover {
  transform: scale(1.03);
}

.image-item img {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.image-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.6);
  color: white;
  padding: 8px;
  display: flex;
  justify-content: space-between;
  font-size: 14px;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  max-width: 90%;
  max-height: 90%;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

.modal-content img {
  max-width: 100%;
  max-height: 70vh;
  display: block;
  margin: 0 auto;
}

.modal-info {
  padding: 20px;
  background: #f9f9f9;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  z-index: 10;
}

.close-btn:hover {
  background: rgba(0, 0, 0, 0.8);
}

.download-btn {
  display: inline-block;
  margin-top: 15px;
  padding: 8px 15px;
  background-color: #2196F3;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.download-btn:hover {
  background-color: #0b7dda;
}
</style>
