<script setup lang="ts">
import { RouterLink } from 'vue-router'
import PageHeader from '@/components/common/PageHeader.vue'
</script>

<template>
  <div class="faq-page">
    <PageHeader title="常见问题" subtitle="帮助您更好地使用舞动银龄平台" />
    
    <ElCard class="faq-content">
      <p class="intro">在这里，我们整理了用户经常提出的问题和相应的解答，希望能够帮助您更好地使用舞动银龄平台。如果您没有找到想要的答案，欢迎通过<RouterLink to="/contact">联系我们</RouterLink>页面与我们取得联系。</p>
      
      <ElCollapse accordion class="faq-collapse">
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">什么是舞动银龄平台？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄是一个专为老年人设计的舞蹈教学与健康管理平台，旨在通过舞蹈活动促进老年人身心健康，丰富晚年生活。平台提供专业的舞蹈教学视频、AI辅助教练、健康管理工具以及社交互动功能，让银龄生活更加精彩。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">如何注册舞动银龄账号？</div>
          </template>
          <div class="faq-content">
            <p>注册舞动银龄账号非常简单，您可以按照以下步骤操作：</p>
            <ol>
              <li>点击网站右上角的"登录/注册"按钮</li>
              <li>选择"注册新账号"</li>
              <li>填写您的手机号码或电子邮箱</li>
              <li>设置密码并完成验证</li>
              <li>填写基本个人信息（可选）</li>
              <li>阅读并同意用户协议和隐私政策</li>
              <li>点击"完成注册"</li>
            </ol>
            <p>注册成功后，您就可以使用舞动银龄的各项功能了。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">平台上的舞蹈课程是免费的吗？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄平台提供两种类型的舞蹈课程：</p>
            <ul>
              <li><strong>免费课程</strong>：平台提供部分基础舞蹈课程和公益课程，所有注册用户均可免费学习。</li>
              <li><strong>付费课程</strong>：由专业舞蹈教师和知名舞蹈家提供的高质量课程，需要付费购买。这些课程通常包含更详细的教学内容、多角度示范视频和个性化反馈。</li>
            </ul>
            <p>此外，我们还会不定期推出优惠活动和会员订阅计划，为用户提供更多优惠。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">AI教练功能如何使用？</div>
          </template>
          <div class="faq-content">
            <p>AI教练是舞动银龄平台的特色功能，可以帮助您评估舞蹈动作并提供改进建议。使用方法如下：</p>
            <ol>
              <li>登录您的账号并进入"AI教练"页面</li>
              <li>选择您想要练习的舞蹈类型</li>
              <li>按照页面提示，使用设备摄像头录制您的舞蹈视频（或上传已有视频）</li>
              <li>等待AI分析完成（通常需要几秒钟）</li>
              <li>查看AI给出的评估结果和改进建议</li>
            </ol>
            <p>请注意，为了获得最佳效果，建议在光线充足的环境下录制视频，并确保您的全身都在画面中。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">如何参与社区互动？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄平台提供丰富的社区互动功能，您可以：</p>
            <ul>
              <li>在社区中分享您的舞蹈视频和照片</li>
              <li>参与每日舞蹈打卡挑战</li>
              <li>加入兴趣小组与志同道合的朋友交流</li>
              <li>参与线上舞蹈活动和比赛</li>
              <li>评论和点赞其他用户的分享</li>
              <li>关注您喜欢的舞蹈老师和其他用户</li>
            </ul>
            <p>通过这些互动，您可以结交新朋友，获得鼓励和支持，让舞蹈学习更加有趣。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">健康管理功能包含哪些内容？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄平台的健康管理功能主要包括：</p>
            <ul>
              <li><strong>运动记录</strong>：自动记录您的舞蹈时长、消耗的卡路里等数据</li>
              <li><strong>健康数据追踪</strong>：可以记录血压、心率、体重等健康指标</li>
              <li><strong>健康评估</strong>：根据您的活动情况和健康数据，提供简单的健康状况评估</li>
              <li><strong>运动建议</strong>：根据您的年龄和健康状况，提供适合的运动建议</li>
              <li><strong>健康知识</strong>：提供老年人健康保健知识</li>
            </ul>
            <p>请注意，平台提供的健康管理功能仅供参考，不能替代专业医疗建议。如有健康问题，请咨询医疗专业人士。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">忘记密码怎么办？</div>
          </template>
          <div class="faq-content">
            <p>如果您忘记了密码，可以通过以下步骤重置：</p>
            <ol>
              <li>在登录页面点击"忘记密码"</li>
              <li>输入您注册时使用的手机号码或电子邮箱</li>
              <li>选择接收验证码的方式（短信或邮件）</li>
              <li>输入收到的验证码</li>
              <li>设置新密码</li>
              <li>使用新密码登录</li>
            </ol>
            <p>如果您在重置密码过程中遇到任何问题，请<RouterLink to="/contact">联系我们</RouterLink>的客服团队获取帮助。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">平台支持哪些支付方式？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄平台支持多种支付方式，包括：</p>
            <ul>
              <li>微信支付</li>
              <li>支付宝</li>
              <li>银联卡支付</li>
              <li>平台余额支付</li>
            </ul>
            <p>所有支付渠道均采用安全加密技术，保障您的支付安全。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">如何保护我的隐私安全？</div>
          </template>
          <div class="faq-content">
            <p>舞动银龄平台高度重视用户隐私保护，我们采取以下措施保护您的个人信息：</p>
            <ul>
              <li>采用加密技术保护您的账号信息和个人数据</li>
              <li>严格控制内部数据访问权限</li>
              <li>不会未经您的同意向第三方分享您的个人信息</li>
              <li>提供隐私设置选项，让您可以控制个人信息的可见范围</li>
            </ul>
            <p>您可以在<RouterLink to="/privacy-policy">隐私政策</RouterLink>中了解更多关于我们如何收集、使用和保护您个人信息的详细内容。</p>
          </div>
        </ElCollapseItem>
        
        <ElCollapseItem>
          <template #title>
            <div class="faq-title">如何取消订阅或退款？</div>
          </template>
          <div class="faq-content">
            <p>如果您需要取消订阅或申请退款，请按照以下步骤操作：</p>
            <ol>
              <li>登录您的账号</li>
              <li>进入"个人中心"->"我的订单"</li>
              <li>找到相应的订单，点击"申请退款"或"取消订阅"</li>
              <li>选择退款原因并提交申请</li>
            </ol>
            <p>请注意，不同类型的产品有不同的退款政策：</p>
            <ul>
              <li>单次购买的课程：在购买后7天内且观看进度不超过30%可申请全额退款</li>
              <li>会员订阅：可随时取消续费，已付费的会员期限内仍可使用服务</li>
            </ul>
            <p>如有特殊情况，请<RouterLink to="/contact">联系客服</RouterLink>处理。</p>
          </div>
        </ElCollapseItem>
      </ElCollapse>
    </ElCard>
  </div>
</template>

<style scoped>
.faq-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto 60px;
}

.faq-content {
  margin-bottom: 40px;
}

.intro {
  font-size: 18px;
  line-height: 1.6;
  margin-bottom: 30px;
  color: var(--el-text-color-secondary);
  text-align: center;
}

.faq-collapse {
  margin-top: 20px;
}

.faq-collapse :deep(.el-collapse-item__header) {
  font-size: 18px;
  padding: 15px;
  background-color: var(--el-fill-color-light);
  border-radius: 4px;
}

.faq-collapse :deep(.el-collapse-item__content) {
  padding: 20px;
  background-color: #fff;
  border-radius: 0 0 4px 4px;
}

.faq-title {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.faq-content {
  color: var(--el-text-color-regular);
  line-height: 1.6;
}

.faq-content p,
.faq-content ul,
.faq-content ol {
  margin-bottom: 15px;
}

.faq-content ul,
.faq-content ol {
  padding-left: 20px;
}

.faq-content li {
  margin-bottom: 8px;
}

.faq-content strong {
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.faq-content a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.faq-content a:hover {
  text-decoration: underline;
}
</style> 