<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import request from '@/utils/request'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const loginFormRef = ref<FormInstance>()

// 将多个协议状态合并为一个
const allAgreed = ref(false)

// 协议弹窗控制
const showAgreementDialog = ref(false)
const currentAgreement = ref<'user' | 'privacy' | 'license' | 'originality'>('user')

// 协议内容
const agreements = {
  user: {
    title: '网站协议',
    content: `
      <p>尊敬的用户，欢迎您使用本网站。在使用本网站前，请仔细阅读以下协议内容。如果您同意以下条款，请点击“同意并继续”按钮，进入本网站。如果您不同意以下条款，请勿使用本网站。</p>
          <h2 class="text-xl font-semibold">一、协议概述</h2>
          <p>1. 本协议是您与网站开发商（以下简称“我们”）之间关于您使用本网站所达成的协议。</p>
          <p>2. 本协议内容包括协议正文及所有我们发布的各类规则。所有规则为本协议不可分割的一部分，与协议正文具有同等法律效力。</p>
          <h2 class="text-xl font-semibold">二、网站使用许可</h2>
          <p>1. 我们授予您一项有限的、非独占的、不可转让的、可撤销的使用本网站的权利。</p>
          <p>2. 您可以在一台或多台设备上安装、使用、显示、运行本网站。</p>
          <p>3. 您不得对本网站进行逆向工程、反编译、反汇编或试图以其他方式发现本网站的源代码。</p>
          <h2 class="text-xl font-semibold">三、用户行为规范</h2>
          <p>1. 您在使用本网站时，应遵守法律法规，不得利用本网站从事违法活动。</p>
          <p>2. 您不得侵犯我们的知识产权，不得传播、上传、发布含有侵权内容的文件。</p>
          <p>3. 您应确保账号和密码的安全，对使用账号和密码所产生的一切后果承担法律责任。</p>
          <h2 class="text-xl font-semibold">四、隐私政策</h2>
          <p>1. 我们尊重您的隐私，承诺不会泄露您的个人信息。</p>
          <p>2. 我们可能会收集和使用您的非个人信息，以优化网站功能和用户体验。</p>
          <p>3. 在特定情况下，我们可能会根据法律法规要求，向有权机关提供您的相关信息。</p>
          <h2 class="text-xl font-semibold">五、免责声明</h2>
          <p>1. 本网站按“现状”提供，我们不承诺本网站的适用性、准确性、可靠性等。</p>
          <p>2. 我们不对因使用本网站导致的任何损失承担责任，包括但不限于直接、间接、偶然、特殊损害。</p>
          <h2 class="text-xl font-semibold">六、协议变更与终止</h2>
          <p>1. 我们有权随时修改本协议，修改后的协议在公布后立即生效。</p>
          <p>2. 在协议变更后，您继续使用本网站即视为同意新的协议内容。</p>
          <p>3. 我们有权在必要时终止本协议，届时您应停止使用本网站。</p>
          <p class="mt-6 text-center font-semibold">请您仔细阅读本协议，点击“同意并继续”按钮表示您已充分了解并接受本协议的全部内容。感谢您的使用！</p>
          <div class="flex justify-center gap-6 mt-4">
            <el-button type="danger">拒绝</el-button>
            <el-button type="primary">同意并继续</el-button>
          </div>
    `
  },
  privacy: {
    title: '隐私保护协议',
    content: `
      <p>欢迎使用舞动银龄（以下简称“本平台”）。我们高度重视用户的隐私保护，并致力于通过本协议向您说明我们如何收集、使用、存储和保护您的个人信息。请您在使用本平台前仔细阅读并理解本协议。如果您不同意本协议的内容，请立即停止使用本平台。</p>
          <h2 class="text-xl font-semibold">一、信息的收集</h2>
          <p>1. 个人信息</p>
          <p>我们可能收集您的以下个人信息：</p>
          <ul class="list-disc ml-6">
            <li>身份信息：如姓名、性别、出生日期、身份证号等；</li>
            <li>联系方式：如电话号码、电子邮件地址、社交账号等；</li>
            <li>账户信息：如用户名、密码、账户ID等；</li>
            <li>设备信息：如IP地址、设备型号、操作系统、浏览器类型等；</li>
            <li>使用信息：如浏览记录、搜索记录、点击行为、访问时间等；</li>
            <li>其他信息：如您主动提交的内容、反馈意见等。</li>
          </ul>
          <p>2. 信息的来源</p>
          <p>我们通过以下方式收集信息：</p>
          <ul class="list-disc ml-6">
            <li>您直接提供的信息；</li>
            <li>您使用本平台时自动生成的信息；</li>
            <li>从第三方合作伙伴获取的信息（如已获得您的授权）。</li>
          </ul>
          <h2 class="text-xl font-semibold">二、信息的使用</h2>
          <p>我们收集的信息将用于以下目的：</p>
          <ul class="list-disc ml-6">
            <li>为您提供、维护和改进本平台的服务；</li>
            <li>验证您的身份，保障账户安全；</li>
            <li>个性化您的使用体验，如推荐内容、广告等；</li>
            <li>与您沟通，如发送通知、回复咨询等；</li>
            <li>进行数据分析、市场研究及服务优化；</li>
            <li>遵守法律法规及平台政策。</li>
          </ul>
          <h2 class="text-xl font-semibold">三、信息的共享与披露</h2>
          <p>我们承诺在未经您同意的情况下，不会将您的个人信息出售、出租或共享给第三方，除非以下情形：</p>
          <ul class="list-disc ml-6">
            <li>为提供服务所需，向我们的合作伙伴、服务提供商或关联方共享必要信息；</li>
            <li>根据法律法规、司法程序或政府要求披露信息；</li>
            <li>为保护本平台、用户或公众的合法权益，防止欺诈、安全威胁等行为；</li>
            <li>在涉及合并、收购或资产转让时，您的信息可能作为交易的一部分被转移。</li>
          </ul>
          <h2 class="text-xl font-semibold">四、信息的存储与保护</h2>
          <p>1. 存储地点</p>
          <p>您的信息将存储于中华人民共和国境内的服务器上。如需跨境传输，我们将确保符合相关法律法规的要求。</p>
          <p>2. 保护措施</p>
          <p>我们采取合理的技术和管理措施保护您的信息安全，包括但不限于加密存储、访问控制、安全审计等。然而，互联网传输和电子存储并非绝对安全，我们无法保证信息的绝对安全。</p>
          <p>3. 存储期限</p>
          <p>我们仅在实现本协议所述目的所需的期限内保留您的信息，超出期限后将予以删除或匿名化处理。</p>
          <h2 class="text-xl font-semibold">五、您的权利</h2>
          <ul class="list-disc ml-6">
            <li>访问与更正：您可以访问和更正您的个人信息；</li>
            <li>删除：您可以要求删除您的个人信息，除非法律法规另有规定；</li>
            <li>撤回同意：您可以撤回对我们处理您个人信息的同意；</li>
            <li>注销账户：您可以申请注销账户，我们将停止处理您的信息；</li>
            <li>投诉与建议：如您对我们的隐私保护措施有疑问或建议，请联系我们。</li>
          </ul>
          <h2 class="text-xl font-semibold">六、未成年人保护</h2>
          <p>本平台不面向未满14周岁的未成年人提供服务。如果我们发现收集了未成年人的个人信息，将立即删除。</p>
          <h2 class="text-xl font-semibold">七、协议的变更</h2>
          <p>我们可能根据法律法规或业务需要更新本协议。更新后的协议将在本平台公布，请您定期查阅。如您继续使用本平台，即视为同意更新后的协议。</p>
          <h2 class="text-xl font-semibold">八、联系我们</h2>
          <p>如您对本协议或隐私保护有任何疑问，请联系我们：</p>
          <p>电子邮件：__________</p>
          <p>联系电话：__________</p>
          <p>联系地址：__________</p>
    `
  },
  license: {
    title: '原创作品授权协议',
    content: `
      <p>甲方（网站提供者）：舞动银龄</p>
          <p>乙方（原创作品作者）：__________________</p>
          <h2 class="text-xl font-semibold">一、协议目的</h2>
          <p>1. 本协议旨在明确甲乙双方在原创作品展播、分享、下载等环节的权利义务关系。</p>
          <p>2. 乙方授权甲方在其平台上展播乙方原创作品，甲方为乙方提供作品展示和推广服务。</p>
          <h2 class="text-xl font-semibold">二、授权内容</h2>
          <p>1. 乙方同意将其原创作品（以下简称"作品"）授权给甲方，甲方有权在以下范围内使用乙方的作品：</p>
          <p>（1）在甲方平台上展示乙方的作品；</p>
          <p>（2）对乙方的作品进行推广、宣传；</p>
          <p>（3）允许用户浏览、下载乙方的作品；</p>
          <p>（4）其他经乙方同意的使用方式。</p>
          <p>2. 乙方授权甲方使用作品的期限为：自本协议签订之日起至乙方书面通知甲方解除授权之日止。</p>
          <h2 class="text-xl font-semibold">三、乙方权利与义务</h2>
          <p>1. 乙方保证其作品为原创作品，拥有完整的知识产权，且未侵犯任何第三方的合法权益。</p>
          <p>2. 乙方同意甲方在协议约定的范围内使用其作品，并保证不将作品授权给其他第三方使用。</p>
          <p>3. 乙方有权要求甲方支付作品使用费，具体费用及支付方式由双方另行约定。</p>
          <p>4. 乙方应确保作品内容符合法律法规，不含有违法、违规信息。</p>
          <h2 class="text-xl font-semibold">四、甲方权利与义务</h2>
          <p>1. 甲方应确保乙方作品在平台上的安全，采取措施防止作品被未经授权的第三方下载、传播。</p>
          <p>2. 甲方有权对乙方作品进行审核，如发现作品不符合本协议规定，甲方有权拒绝展播或删除作品。</p>
          <p>3. 甲方应尊重乙方的知识产权，不得擅自修改、歪曲乙方作品。</p>
          <h2 class="text-xl font-semibold">五、协议的变更与终止</h2>
          <p>1. 双方同意，本协议的变更、解除、终止等事宜，应以书面形式确认。</p>
          <p>2. 乙方有权在提前通知甲方的情况下，解除本协议。协议解除后，甲方应停止使用乙方的作品。</p>
          <h2 class="text-xl font-semibold">六、争议解决</h2>
          <p>1. 本协议的签订、履行、解释及争议解决均适用中华人民共和国法律法规。</p>
          <p>2. 如双方在协议履行过程中发生争议，应首先通过友好协商解决；协商不成的，任何一方均有权向甲方所在地人民法院提起诉讼。</p>
          <p class="mt-4">乙方签字（或盖章）：____________________</p>
          <p>签订日期：______________________________</p>
          <p class="mt-4">请乙方下载本协议文件，签字或盖章后上传至甲方平台。甲方审核通过后，乙方即可上传作品。感谢您的支持与合作！</p>
          <p class="mt-4">甲方（网站提供者）：舞动银龄</p>
          <p>地址：______________________________</p>
          <p>联系人：______________________________</p>
          <p>联系电话：______________________________</p>
          <p>电子邮箱：______________________________</p>
    `
  },
  originality: {
    title: '原创性保证书',
    content: `
      <p>本人（用户姓名/用户名），身份证号/用户ID：__________，作为舞动银龄的用户，在此郑重承诺并保证如下：</p>
          <h2 class="text-xl font-semibold">一、原创性声明</h2>
          <p>本人通过舞动银龄上传、发布、提交或分享的所有内容（包括但不限于文字、图片、音频、视频、代码等）均为本人原创，未抄袭、复制、改编或侵犯任何第三方的知识产权（包括但不限于版权、商标权、专利权等）。</p>
          <h2 class="text-xl font-semibold">二、权利归属</h2>
          <p>本人对上述内容拥有完整、合法的权利，并有权授权舞动银龄按照其服务条款及相关协议使用该内容。</p>
          <h2 class="text-xl font-semibold">三、无侵权保证</h2>
          <p>本人保证上述内容不会侵犯任何第三方的合法权益，包括但不限于知识产权、肖像权、隐私权、名誉权等。若因本人提供的内容引发任何法律纠纷或索赔，本人将承担全部责任，并赔偿舞动银龄及其关联方因此遭受的全部损失。</p>
          <h2 class="text-xl font-semibold">四、责任承担</h2>
          <p>如因本人违反本保证书的内容，导致舞动银龄遭受任何损失、索赔或处罚，本人愿意承担全部法律责任，包括但不限于赔偿损失、支付违约金、承担诉讼费用等。</p>
          <h2 class="text-xl font-semibold">五、授权使用</h2>
          <p>本人同意舞动银龄在遵守相关法律法规及隐私政策的前提下，对本人上传的内容进行存储、展示、传播、修改（如必要）及其他合法使用。</p>
          <h2 class="text-xl font-semibold">六、保证书的效力</h2>
          <p>本保证书自本人签署之日起生效，具有法律效力。本人理解并同意，舞动银龄有权根据本保证书采取相应措施，包括但不限于删除侵权内容、暂停或终止本人的账户权限等。</p>
          <h2 class="text-xl font-semibold">七、其他</h2>
          <p>本保证书的解释、效力及争议解决均适用中华人民共和国法律。如因本保证书产生争议，双方应友好协商解决；协商不成的，任何一方均可向舞动银龄所在地有管辖权的人民法院提起诉讼。</p>
          <p class="mt-4">特此保证！</p>
          <p>用户姓名/用户名：__________</p>
          <p>签署日期：__________</p>
          <p class="italic">（电子签名/手写签名）</p>
    `
  }
}

// 打开协议弹窗
const openAgreement = (type: 'user' | 'privacy' | 'license' | 'originality') => {
  currentAgreement.value = type
  showAgreementDialog.value = true
}

interface LoginForm {
  username: string
  password: string
  remember: boolean
}

const loginForm = reactive<LoginForm>({
  username: '',
  password: '',
  remember: false
})

const rules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少为6个字符', trigger: 'blur' }
  ]
})

const handleLogin = async () => {
  if (!loginFormRef.value) return

  // 检查是否同意所有协议
  if (!allAgreed.value) {
    ElMessage.warning('请阅读并同意所有用户协议后登录')
    return
  }
  
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        const result = await userStore.login({
          username: loginForm.username,
          password: loginForm.password
        })
        
        if (result) {
          ElMessage.success('登录成功')
          
          // 重定向到之前的页面或首页
          const redirectPath = route.query.redirect as string || '/'
          await router.replace(redirectPath)
        }
      } catch (error) {
        console.error('Login failed:', error)
      } finally {
        loading.value = false
      }
    }
  })
}

const demoLogin = async () => {
  // 自动同意所有协议
  allAgreed.value = true
  
  loading.value = true
  try {
    // 使用演示登录方法，不需要服务器验证
    const result = userStore.demoLogin()
    
    if (result) {
      // 重定向到之前的页面或首页
      const redirectPath = route.query.redirect as string || '/'
      await router.replace(redirectPath)
    }
  } catch (error) {
    console.error('Demo login failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="background-orb orb1"></div>
    <div class="background-orb orb2"></div>
    
    <ElCard class="login-card">
      <h2 class="login-title">舞动银龄 - 用户登录</h2>
      
      <ElForm
        ref="loginFormRef"
        :model="loginForm"
        :rules="rules"
        label-position="top"
        @submit.prevent="handleLogin"
      >
        <ElFormItem label="用户名" prop="username">
          <ElInput v-model="loginForm.username" placeholder="请输入用户名"></ElInput>
        </ElFormItem>
        
        <ElFormItem label="密码" prop="password">
          <ElInput
            v-model="loginForm.password"
            placeholder="请输入密码"
            type="password"
            show-password
          ></ElInput>
        </ElFormItem>
        
        <ElFormItem>
          <ElCheckbox v-model="loginForm.remember">记住我</ElCheckbox>
        </ElFormItem>
        
        <div class="agreements-section-integrated">
          <ElCheckbox v-model="allAgreed">
            <span class="agreement-text">
              我已阅读并同意
              <ElLink type="primary" @click.prevent="openAgreement('user')">《网站协议》</ElLink>
              <ElLink type="primary" @click.prevent="openAgreement('privacy')">《隐私保护协议》</ElLink>
              <ElLink type="primary" @click.prevent="openAgreement('license')">《原创作品授权协议》</ElLink>
              <ElLink type="primary" @click.prevent="openAgreement('originality')">《原创性保证书》</ElLink>
            </span>
          </ElCheckbox>
        </div>
        
        <ElFormItem>
          <ElButton type="primary" native-type="submit" :loading="loading" class="login-button">
            登录
          </ElButton>
        </ElFormItem>
        
        <div class="demo-login">
          <ElButton type="success" @click="demoLogin" :loading="loading">
            使用演示账号登录
          </ElButton>
        </div>
        
        <div class="register-link">
          没有账号？<ElLink type="primary" href="/register">立即注册</ElLink>
        </div>
      </ElForm>
    </ElCard>

    <!-- 协议弹窗 -->
    <ElDialog
      v-model="showAgreementDialog"
      :title="agreements[currentAgreement].title"
      width="600px"
      class="agreement-dialog"
    >
      <div class="agreement-content" v-html="agreements[currentAgreement].content"></div>
      <template #footer>
        <ElButton @click="showAgreementDialog = false">关闭</ElButton>
      </template>
    </ElDialog>
  </div>
</template>

<style scoped>
.login-container {
  position: relative;
  min-height: 100vh;
  padding-top: 64px;
  padding-bottom: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(45deg, #f7d060 0%, #a57c00 100%);
  overflow: hidden;
  z-index: 1;
}

@media (max-width: 640px) {
  .login-container {
    padding-top: 20px;
    padding-bottom: 80px;
  }
}

.background-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  z-index: 0;
}

.orb1 {
  width: 400px;
  height: 400px;
  background-color: rgba(255, 230, 150, 0.7);
  top: 5%;
  left: 10%;
  animation: moveOrb1 20s infinite alternate;
}

.orb2 {
  width: 450px;
  height: 450px;
  background-color: rgba(255, 190, 80, 0.5);
  bottom: 10%;
  right: 15%;
  animation: moveOrb2 25s infinite alternate-reverse;
}

@keyframes moveOrb1 {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(100px, -120px) scale(1.1); }
}

@keyframes moveOrb2 {
  from { transform: translate(0, 0) scale(1); }
  to { transform: translate(-80px, 90px) scale(0.9); }
}

.login-card {
  width: 400px;
  max-width: 90%;
  background: rgba(255, 255, 255, 0.25);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
  border-radius: 20px;
  position: relative;
  z-index: 1;
  transition: all 0.3s ease;
  margin: 20px 0;
}

.login-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.3);
}

.login-title {
  text-align: center;
  margin: 0 0 30px 0;
  font-size: 24px;
  color: #5a4620;
  text-shadow: 0 2px 4px rgba(255, 255, 255, 0.5);
  font-weight: 600;
}

.login-button {
  width: 100%;
}

.agreements-section-integrated {
  margin-bottom: 22px;
}

/* --- 修改开始 --- */
.agreements-section-integrated :deep(.el-checkbox) {
  /* 确保复选框容器不会限制内部文本的换行 */
  height: auto;
  /* 关键：让复选框的方块与多行文本的顶部对齐 */
  align-items: flex-start;
}

.agreements-section-integrated :deep(.el-checkbox__label) {
  /* 关键：允许文本换行 */
  white-space: normal;
}

.agreements-section-integrated .agreement-text {
  font-size: 13px;
  color: #606266;
  line-height: 1.6; /* 调整行高，让换行后更美观 */
}
/* --- 修改结束 --- */


.agreements-section-integrated :deep(.el-link) {
  vertical-align: baseline;
}

.demo-login {
  margin-top: 20px;
  text-align: center;
}

.register-link {
  margin-top: 15px;
  text-align: center;
}

@media (max-width: 480px) {
  .login-card {
    width: 320px;
  }
}

/* 协议弹窗样式 */
.agreement-content {
  max-height: 400px;
  overflow-y: auto;
  padding: 10px;
  line-height: 1.8;
}

.agreement-content :deep(h3) {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 20px 0 10px 0;
}

.agreement-content :deep(h3:first-child) {
  margin-top: 0;
}

.agreement-content :deep(p) {
  margin: 8px 0;
  color: #606266;
  text-indent: 0;
}
</style>