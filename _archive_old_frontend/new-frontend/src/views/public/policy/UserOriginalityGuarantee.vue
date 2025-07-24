<template>
  <el-scrollbar height="100vh" class="py-8 px-4">
    <el-card class="mx-auto max-w-4xl">
      <h1 class="text-center text-2xl font-bold mb-6">原创性保证书</h1>
      <div class="space-y-4 leading-7">
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
      </div>
    </el-card>
  </el-scrollbar>
</template>

<script setup lang="ts">
import { useTitle } from '@vueuse/core'
useTitle('原创性保证书 - 舞动银龄')
</script> 