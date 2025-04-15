<template>
  <footer class="app-footer">
    <div class="container">
      <el-row :gutter="20">
        <el-col :span="8">
          <h5>舞动银龄</h5>
          <p>专为老年人设计的舞蹈教学与健康管理平台，让银龄生活更精彩。</p>
        </el-col>
        <el-col :span="4">
          <div class="footer-links">
            <ul>
              <li><router-link to="/">首页</router-link></li>
              <li><router-link to="/coach">AI教练</router-link></li>
              <li><router-link to="/health">健康管理</router-link></li>
              <li><router-link to="/social">社交平台</router-link></li>
              <li><router-link to="/about">关于我们</router-link></li>
            </ul>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="footer-links">
            <ul>
              <li><router-link to="/faq">常见问题</router-link></li>
              <li><router-link to="/contact">联系我们</router-link></li>
              <li><router-link to="/privacy-policy">隐私政策</router-link></li>
              <li><router-link to="/user-agreement">用户协议</router-link></li>
              <li><router-link to="/originality-guarantee">原创性保证</router-link></li>
              <li><router-link to="/original-license">原创授权协议</router-link></li>
            </ul>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="footer-links">
            <h5>联系我们</h5>
            <ul>
              <li><el-icon><Message /></el-icon> contact@wdyl.cnies.org</li>
              <li><el-icon><Location /></el-icon> 山东省济南市</li>
            </ul>
            <div class="social-links">
              <a href="#"><el-icon><ElementPlus /></el-icon></a>
              <a href="#"><el-icon><Share /></el-icon></a>
              <a href="#"><el-icon><ChatDotRound /></el-icon></a>
            </div>
          </div>
        </el-col>
      </el-row>
      <div class="copyright">
        <p>&copy; 2025 舞动银龄 版权所有</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { Message, Location, ElementPlus, Share, ChatDotRound } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
.app-footer {
  background-color: #333333;
  color: white;
  padding: 50px 0 20px;

  h5 {
    font-size: 20px;
    margin-bottom: 20px;
  }

  p {
    color: #ccc;
    font-size: 18px;
  }

  .footer-links {
    ul {
      list-style: none;
      padding: 0;
      margin: 0;

      li {
        margin-bottom: 10px;
        font-size: 18px;

        a {
          color: #ccc;
          text-decoration: none;
          transition: color 0.3s;
          font-size: 18px;

          &:hover {
            color: white;
          }
        }

        .el-icon {
          margin-right: 8px;
          color: var(--primary-color);
        }
      }
    }
  }

  .social-links {
    margin-top: 20px;
    display: flex;
    gap: 15px;

    a {
      color: #ccc;
      font-size: 24px;
      transition: color 0.3s;

      &:hover {
        color: white;
      }
    }
  }

  .copyright {
    border-top: 1px solid #444;
    margin-top: 30px;
    padding-top: 20px;
    text-align: center;
    color: #ccc;
  }
}
</style>