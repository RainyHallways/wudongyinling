<template>
  <div class="agreement-page">
    <div class="container">
      <h1 class="page-title">原创性保证协议</h1>
      
      <el-card class="agreement-content">
        <p class="intro">本人（用户姓名/用户ID）____________ 作为 ____________ 平台/系统用户的创作者，在此郑重声明：</p>
        
        <div class="section">
          <h2>1. 原创声明</h2>
          <p>本人保证提交到平台/系统的所有、图像、视频或其他形式的内容是本人独立创作、原创、自主研发的作品，不存在抄袭、剽窃、篡改或侵犯他人知识产权及相关权利（包括但不限于著作权、肖像权、名誉权等）的情况。</p>
        </div>
        
        <div class="section">
          <h2>2. 权利归属</h2>
          <p>本人对所提交内容拥有合法、完整的权利，有权授权平台/系统使用该内容，且该授权不会侵犯任何第三方的合法权益。</p>
        </div>
        
        <div class="section">
          <h2>3. 知识产权保证</h2>
          <p>本人保证所提交内容不侵犯他人知识产权的任何形式，包括但不限于著作权、商标权、专利权、商业秘密等。若本人提交的内容存在侵权嫌疑，本人愿意承担相应的法律责任，并赔偿因此给平台/系统造成的损失。</p>
        </div>
        
        <div class="section">
          <h2>4. 侵权责任</h2>
          <p>若本人违反本原创性保证协议，平台/系统有权采取相应措施，包括但不限于删除相关内容、暂停或终止账号使用权、追究法律责任、要求赔偿损失等。</p>
        </div>
        
        <div class="section">
          <h2>5. 授权使用</h2>
          <p>本人同意平台/系统在合法合规且符合平台规则的前提下，对本人提交的内容进行展示、推广、传播、存储等操作，以实现平台功能。</p>
        </div>
        
        <div class="section">
          <h2>6. 原创性的核实</h2>
          <p>本原创性保证是本人真实意愿的表达，本人同意平台/系统有权通过技术手段核实本原创性保证的真实性，包括但不限于内容查重、版权检测、人工审核等。</p>
        </div>
        
        <div class="section">
          <h2>7. 其他</h2>
          <p>本原创性保证的解释、效力与履行适用中华人民共和国法律。如本原创性保证与任何法律规定相抵触，应以相关法律规定为准，但不影响本保证其他条款的效力。</p>
        </div>
        
        <p class="conclusion">特此保证！</p>
        
        <div class="signature-section">
          <div class="signature-item">
            <p>用户姓名/用户ID：______________</p>
          </div>
          <div class="signature-item">
            <p>签名日期：______________</p>
          </div>
          <div class="signature-item">
            <p>电话号码/联系方式：</p>
          </div>
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
  padding: 40px 0;
}

.page-title {
  text-align: center;
  margin-bottom: 30px;
  color: var(--primary-color);
  font-size: 28px;
}

.agreement-content {
  margin-bottom: 40px;
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
  margin: 8px 0; /* 从10px改为8px，减少标题上下间距 */
  color: var(--primary-color);
  padding-top: 8px; /* 从10px改为8px，减少上部内边距 */
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

.signature-section {
  margin-top: 30px; /* 从40px改为30px，减少签名区域与上方内容的间距 */
  display: flex;
  flex-direction: column;
  gap: 12px; /* 从15px改为12px，减少签名项之间的间距 */
}

.signature-item {
  margin-bottom: 8px; /* 从10px改为8px，减少签名项底部间距 */
}
</style>