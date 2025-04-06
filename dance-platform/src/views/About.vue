<template>
  <div class="about">
    <h1 class="page-title">关于舞动银龄</h1>

    <!-- 公司介绍 -->
    <el-card class="about-section">
      <h2>我们的故事</h2>
      <p>"舞动银龄"成立于2023年，是一个专为老年人设计的舞蹈教学和智能纠错平台。我们的初衷是帮助老年人通过舞蹈保持身心健康，享受舞蹈带来的快乐，同时促进老年人之间的社交互动。</p>
      <p>我们团队由舞蹈教育专家、健康医疗专业人士、人工智能工程师和老年服务管理人员组成。我们共同努力，将传统舞蹈教学与现代科技相结合，创造一个友好、安全且有效的舞蹈学习环境。</p>
      <p>经过多年发展，"舞动银龄"已经服务了超过10万名老年用户，开设了200多门针对不同健康状况和舞蹈水平的课程，成为中国领先的老年舞蹈教育平台。</p>
    </el-card>

    <!-- 使命和愿景 -->
    <el-row :gutter="20" class="mission-vision">
      <el-col :span="12">
        <el-card class="mission">
          <h2>我们的使命</h2>
          <p>通过结合科技与艺术，为老年人提供安全、有效且愉悦的舞蹈学习体验，促进身心健康，丰富晚年生活，搭建社交平台，传承非物质文化遗产。</p>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="vision">
          <h2>我们的愿景</h2>
          <p>成为中国最具影响力的老年舞蹈教育平台，服务1000万老年用户，让每一位银发族群都能享受到适合自己的舞蹈教学资源，实现积极健康的老龄化生活方式。</p>
        </el-card>
      </el-col>
    </el-row>

    <!-- 核心团队 -->
    <el-card class="team-section">
      <h2>核心团队</h2>
      <el-row :gutter="20">
        <el-col :span="6" v-for="member in teamMembers" :key="member.name">
          <div class="team-member">
            <el-avatar :src="member.avatar" :size="150" class="member-photo" />
            <h3 class="member-name">{{ member.name }}</h3>
            <p class="member-title">{{ member.title }}</p>
            <p class="member-bio">{{ member.bio }}</p>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <!-- 合作伙伴 -->
    <el-card class="partners-section">
      <h2>合作伙伴</h2>
      <div class="partners-logos">
        <el-image
          v-for="partner in partners"
          :key="partner.name"
          :src="partner.logo"
          :alt="partner.name"
          class="partner-logo"
          fit="contain"
        />
      </div>
    </el-card>

    <!-- 联系我们 -->
    <el-card class="contact-section">
      <h2>联系我们</h2>
      <el-row :gutter="30">
        <el-col :span="6" v-for="contact in contactInfo" :key="contact.title">
          <div class="contact-item">
            <div class="contact-icon">
              <el-icon :size="24">
                <component :is="contact.icon" />
              </el-icon>
            </div>
            <div class="contact-text">
              <h3>{{ contact.title }}</h3>
              <p>{{ contact.content }}</p>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import {
  Location,
  Phone,
  Message,
  Clock
} from '@element-plus/icons-vue'

// 核心团队数据
const teamMembers = ref([
  {
    name: '张明',
    title: '创始人 & CEO',
    bio: '北京舞蹈学院毕业，拥有20年舞蹈教学经验，致力于推广适合老年人的舞蹈教育。',
    avatar: '/images/zym.png'
  },
  {
    name: '李芳',
    title: '首席健康顾问',
    bio: '资深康复医师，专注老年人运动康复与健康管理，中国老年医学会会员。',
    avatar: '/images/lf.png'
  },
  {
    name: '王科',
    title: '技术总监',
    bio: '人工智能与计算机视觉专家，负责平台舞蹈动作识别与纠正系统的研发。',
    avatar: '/images/wk.png'
  },
  {
    name: '刘婷',
    title: '舞蹈课程总监',
    bio: '国家一级舞蹈编导，专注民族舞蹈教学与研究，负责平台舞蹈课程设计。',
    avatar: '/images/lt.png'
  }
])

// 合作伙伴数据
const partners = ref([
  {
    name: '中国老年保健协会',
    logo: '/images/partners/partner1.png'
  },
  {
    name: '北京舞蹈学院',
    logo: '/images/partners/partner2.png'
  },
  {
    name: '国家非物质文化遗产保护中心',
    logo: '/images/partners/partner3.png'
  },
  {
    name: '中国社区健康促进会',
    logo: '/images/partners/partner4.png'
  },
  {
    name: '智能科技研究院',
    logo: '/images/partners/partner5.png'
  }
])

// 联系方式数据
const contactInfo = ref([
  {
    icon: 'Location',
    title: '地址',
    content: '北京市海淀区中关村南大街5号'
  },
  {
    icon: 'Phone',
    title: '电话',
    content: '400-123-4567'
  },
  {
    icon: 'Message',
    title: '邮箱',
    content: 'info@wudongylng.com'
  },
  {
    icon: 'Clock',
    title: '客服时间',
    content: '周一至周日 9:00-21:00'
  }
])
</script>

<style scoped>
.about {
  padding: 20px;
}

.page-title {
  font-size: 32px;
  text-align: center;
  margin: 40px 0;
  color: var(--primary-color);
}

.about-section {
  margin-bottom: 40px;
}

.about-section h2 {
  font-size: 28px;
  color: var(--primary-color);
  margin-bottom: 20px;
}

.about-section p {
  margin-bottom: 20px;
  font-size: 18px;
  line-height: 1.6;
}

.mission-vision {
  margin: 40px 0;
}

.mission h2,
.vision h2 {
  font-size: 28px;
  color: var(--primary-color);
  margin-bottom: 20px;
  text-align: center;
}

.team-section {
  margin-bottom: 40px;
}

.team-section h2 {
  font-size: 28px;
  color: var(--primary-color);
  margin-bottom: 30px;
  text-align: center;
}

.team-member {
  text-align: center;
  margin-bottom: 30px;
}

.member-photo {
  margin-bottom: 15px;
  border: 5px solid var(--el-border-color-lighter);
}

.member-name {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 5px;
}

.member-title {
  font-size: 18px;
  color: var(--primary-color);
  margin-bottom: 10px;
}

.member-bio {
  font-size: 16px;
  color: #666;
}

.partners-section {
  margin-bottom: 40px;
}

.partners-section h2 {
  font-size: 28px;
  color: var(--primary-color);
  margin-bottom: 30px;
  text-align: center;
}

.partners-logos {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 40px;
}

.partner-logo {
  width: 150px;
  height: 100px;
  object-fit: contain;
}

.contact-section h2 {
  font-size: 28px;
  color: var(--primary-color);
  margin-bottom: 30px;
  text-align: center;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}

.contact-icon {
  width: 50px;
  height: 50px;
  background-color: var(--primary-color);
  color: white;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.contact-text h3 {
  font-size: 20px;
  margin-bottom: 5px;
}

.contact-text p {
  color: #666;
}

@media (max-width: 768px) {
  .page-title {
    font-size: 28px;
  }

  .about-section h2,
  .mission h2,
  .vision h2,
  .team-section h2,
  .partners-section h2,
  .contact-section h2 {
    font-size: 24px;
  }

  .member-name {
    font-size: 20px;
  }

  .member-title {
    font-size: 16px;
  }

  .member-bio {
    font-size: 14px;
  }
}
</style> 