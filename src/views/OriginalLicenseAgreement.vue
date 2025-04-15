<template>
  <div class="agreement-page">
    <div class="container">
      <h1 class="page-title">原创授权协议</h1>
      
      <el-card class="agreement-content">
        <p class="intro">本授权协议由作品原创者（以下简称"原创者"）与平台运营方（以下简称"平台"）签订。</p>
        <p>原创者姓名/机构名称：_______________________</p>
        <p>本协议是关于原创者授权平台使用其原创作品的约定。</p>
        
        <div class="section">
          <h2>一、协议目的</h2>
          <ol>
            <li>本协议旨在明确原创者在平台上传、发布、展示等行为中的权利义务关系。</li>
            <li>原创者与平台在本协议框架下建立授权使用原创作品的合作关系。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>二、授权内容</h2>
          <ol>
            <li>原创者授予平台以下权利（非排他性授权）：
              <ul>
                <li>在平台上展示原创者的作品；</li>
                <li>对原创者的作品进行宣传；</li>
                <li>经原创者同意，对作品进行必要的编辑；</li>
                <li>其他经原创者同意的使用方式。</li>
              </ul>
            </li>
            <li>原创者授权平台使用作品的期限为本协议签订之日起，原创者可随时通知平台终止授权。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>三、原创者权利与义务</h2>
          <ol>
            <li>原创者保证其提供的作品为原创作品，不存在抄袭、剽窃他人作品或侵犯他人知识产权的情况。</li>
            <li>原创者保证在平台授权范围内使用其作品不会侵犯任何第三方的合法权益。</li>
            <li>原创者有权随时要求平台删除作品或停止对作品的使用并终止本协议。</li>
            <li>原创者承诺对作品内容的真实性、合法性负全部责任。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>四、平台权利与义务</h2>
          <ol>
            <li>平台承诺对原创者作品在使用过程中的完整性、原创性给予尊重，不得擅自篡改作品内容。</li>
            <li>平台有权对原创者作品进行审核，并有权拒绝展示违反本协议的作品。平台有权在必要时删除作品。</li>
            <li>平台应尊重原创者的著作人身权，并保护原创者作品。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>五、协议的生效与终止</h2>
          <ol>
            <li>本协议自双方签字、盖章之日起生效，协议终止、解除、变更等需双方协商一致。</li>
            <li>原创者可在告知平台的情况下，随时终止本协议。协议终止后，平台应停止使用原创者的作品。</li>
          </ol>
        </div>
        
        <div class="section">
          <h2>六、争议解决</h2>
          <ol>
            <li>本协议的订立、执行和解释及争议的解决均应适用中华人民共和国法律。</li>
            <li>如双方就本协议内容或执行发生争议，应首先通过友好协商解决；协商不成时，任何一方均可向有管辖权的人民法院提起诉讼。</li>
          </ol>
        </div>
        
        <p class="conclusion">原创者已阅读并理解本协议所有条款，点击"同意并继续"按钮即表示原创者完全接受本协议。</p>
        
        <div class="signature-section">
          <div class="signature-row">
            <div class="signature-item">
              <p>原创者签名：___________________</p>
              <p>签署日期：___________________</p>
            </div>
            <div class="signature-item">
              <p>平台（盖章）：___________________</p>
              <p>签署日期：___________________</p>
              <p>联系电话：___________________</p>
              <p>电子邮箱：___________________</p>
            </div>
          </div>
        </div>
        
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
  margin: 20px 0;
  line-height: 1.8;
}

.section {
  margin: 20px 0; /* 从30px改为20px */
}

.section h2 {
  font-size: 22px;
  margin: 8px 0;
  color: var(--primary-color);
}

/* 优化段落间距 */
.section > p {
  margin: 10px 0;
}

/* 调整列表间距 */
.section ol,
.section ul {
  margin: 10px 0;
  padding-left: 20px;
}

.section li {
  margin-bottom: 10px;
}

.section ul {
  padding-left: 20px;
  margin: 10px 0;
}

.signature-section {
  margin-top: 10px;
}

.signature-row {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}

.signature-item {
  flex: 1;
  min-width: 300px;
}

.agreement-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

@media (max-width: 768px) {
  .signature-row {
    flex-direction: column;
  }
}
</style>