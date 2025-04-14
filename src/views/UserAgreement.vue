<template>
  <div class="agreement-page">
    <div class="container">
      <h1 class="page-title">用户协议</h1>
      
      <el-card class="agreement-content">
        <p class="intro">尊敬的用户，欢迎您使用本网站。在使用本网站前，请仔细阅读以下协议内容。如果您同意以下条款，请点击"同意并继续"按钮，进入本网站。如果您不同意以下条款，请勿使用本网站。</p>
        
        <div class="section">
          <h2>一、协议概述</h2>
          <ol>
            <li>本协议是您与网站开发商（以下简称"我们"）之间关于您使用本网站所达成的协议。</li>
            <li>本协议内容包括协议正文及所有我们发布的各类规则。所有规则为本协议不可分割的一部分，与协议正文具有同等法律效力。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>二、网站使用许可</h2>
          <ol>
            <li>我们授予您一项有限的、非独占的、不可转让的、可撤销的使用本网站的权利。</li>
            <li>您可以在一台或多台设备上安装、使用、显示、运行本网站。</li>
            <li>您不得对本网站进行逆向工程、反编译、反汇编或试图以其他方式发现本网站的源代码。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>三、用户行为规范</h2>
          <ol>
            <li>您在使用本网站时，应遵守法律法规，不得利用本网站从事违法活动。</li>
            <li>您不得侵犯我们的知识产权，不得传播、上传、发布含有侵权内容的文件。</li>
            <li>您应确保账号和密码的安全，对使用账号和密码所产生的一切后果承担法律责任。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>四、隐私政策</h2>
          <ol>
            <li>我们尊重您的隐私，承诺不会泄露您的个人信息。</li>
            <li>我们可能会收集和使用您的非个人信息，以优化网站功能和用户体验。</li>
            <li>在特定情况下，我们可能会根据法律法规要求，向有权机关提供您的相关信息。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>五、免责声明</h2>
          <ol>
            <li>本网站按"现状"提供，我们不承诺本网站的适用性、准确性、可靠性等。</li>
            <li>我们不对因使用本网站导致的任何损失承担责任，包括但不限于直接、间接、偶然、特殊损害。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>六、协议变更与终止</h2>
          <ol>
            <li>我们有权随时修改本协议，修改后的协议在公布后立即生效。</li>
            <li>在协议变更后，您继续使用本网站即视为同意新的协议内容。</li>
            <li>我们有权在必要时终止本协议，届时您应停止使用本网站。</li>
          </ol>
        </div>
        
        <p class="conclusion">请您仔细阅读本协议，点击"同意并继续"按钮表示您已充分了解并接受本协议的全部内容。感谢您的使用！</p>
        
        <div class="agreement-buttons">
          <el-button type="default" size="large">拒绝</el-button>
          <el-button type="primary" size="large">同意并继续</el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
// 无需额外的脚本逻辑
</script>

<style scoped>
.agreement-page {
  padding: 20px 0;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary-color);
  font-size: 28px;
}

.agreement-content {
  margin-bottom: 10px;
  font-size: 18px;
  line-height: 1.8;
}

.intro, .conclusion {
  margin: 16px 0; /* 从20px改为16px，使页面更紧凑 */
  line-height: 1.8;
}

.section {
  margin: 16px 0; /* 从20px改为16px，使各部分更紧凑 */
}

.section h2 {
  font-size: 22px;
  margin: 8px 0;
  color: var(--primary-color);
}

/* 优化段落间距 */
.section > p {
  margin: 8px 0; /* 从10px改为8px，减少段落间距 */
}

/* 调整列表间距 */
.section ol,
.section ul {
  margin: 8px 0; /* 从10px改为8px，减少列表间距 */
  padding-left: 20px;
}

/* 调整小节标题间距 */
.subsection {
  margin: 12px 0; /* 从15px改为12px，进一步减少间距 */
}

.subsection h3 {
  font-size: 20px;
  margin: 8px 0; /* 从margin-bottom: 10px改为margin: 8px 0 */
  color: #333;
}
</style>