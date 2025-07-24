<template>
  <el-scrollbar height="100vh" class="py-8 px-4">
    <el-card class="mx-auto max-w-4xl">
      <h1 class="text-center text-2xl font-bold mb-6">网站协议</h1>
      <div class="space-y-4 leading-7">
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
      </div>
    </el-card>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { useTitle } from '@vueuse/core'
useTitle('网站协议 - 舞动银龄')
</script> 