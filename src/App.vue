<script setup>
import { onMounted, reactive, ref } from 'vue'
import { api } from './api'

const form = reactive({
  name: '',
  goal: '',
  channel: '',
  audience: '',
  budget: '5000/月',
  metadataJson: '{"campaign":"618"}'
})

const tasks = ref([])
const executions = ref([])
const automations = ref([])
const loading = ref(false)

async function loadAll() {
  const [taskRes, executionRes, automationRes] = await Promise.all([
    api.get('/tasks'),
    api.get('/executions'),
    api.get('/automations')
  ])
  tasks.value = taskRes.data
  executions.value = executionRes.data
  automations.value = automationRes.data
}

async function createTask() {
  loading.value = true
  try {
    await api.post('/tasks', form)
    form.name = ''
    form.goal = ''
    form.channel = ''
    form.audience = ''
    form.budget = '5000/月'
    form.metadataJson = '{"campaign":"618"}'
    await loadAll()
  } finally {
    loading.value = false
  }
}

async function runTask(taskId) {
  await api.post(`/tasks/${taskId}/run`)
  await loadAll()
}

async function createAutomation(taskId) {
  await api.post('/automations', {
    taskId,
    name: `任务 ${taskId} 每小时自动执行`,
    intervalMinutes: 60,
    enabled: true
  })
  await loadAll()
}

function pretty(json) {
  return json || '{}'
}

onMounted(loadAll)
</script>

<template>
  <div class="page">
    <aside class="hero">
      <div class="hero-inner">
        <p class="eyebrow">Vue 3 + Spring Boot</p>
        <h1>多 Agent 协同运营自动化系统</h1>
        <p class="hero-copy">
          面向运营团队的任务编排面板。输入目标后，由规划、研究、文案、审查、发布五类 agent 自动协同输出执行结果。
        </p>
      </div>
    </aside>

    <main class="content">
      <section class="card">
        <div class="section-head">
          <h2>创建运营任务</h2>
          <button class="ghost" @click="loadAll">刷新数据</button>
        </div>
        <form class="task-form" @submit.prevent="createTask">
          <input v-model="form.name" placeholder="任务名称" required />
          <input v-model="form.goal" placeholder="目标，例如 提升活动报名转化" required />
          <input v-model="form.channel" placeholder="渠道，例如 小红书" required />
          <input v-model="form.audience" placeholder="目标人群" required />
          <input v-model="form.budget" placeholder="预算" required />
          <textarea v-model="form.metadataJson" rows="3" placeholder="扩展元数据 JSON"></textarea>
          <button :disabled="loading" type="submit">{{ loading ? '提交中...' : '创建任务' }}</button>
        </form>
      </section>

      <section class="card">
        <div class="section-head">
          <h2>任务列表</h2>
          <span class="count">{{ tasks.length }} 项</span>
        </div>
        <div class="stack">
          <article v-for="task in tasks" :key="task.id" class="panel">
            <div class="panel-top">
              <h3>{{ task.name }}</h3>
              <span class="badge">{{ task.channel }}</span>
            </div>
            <p>目标：{{ task.goal }}</p>
            <p>人群：{{ task.audience }}</p>
            <p>预算：{{ task.budget }}</p>
            <div class="actions">
              <button @click="runTask(task.id)">立即执行</button>
              <button class="ghost" @click="createAutomation(task.id)">每小时自动执行</button>
            </div>
          </article>
        </div>
      </section>

      <section class="grid-two">
        <section class="card">
          <div class="section-head">
            <h2>执行记录</h2>
            <span class="count">{{ executions.length }} 条</span>
          </div>
          <div class="stack">
            <article v-for="execution in executions" :key="execution.id" class="panel">
              <div class="panel-top">
                <h3>执行 #{{ execution.id }}</h3>
                <span class="badge success">{{ execution.status }}</span>
              </div>
              <p>任务 ID：{{ execution.taskId }}</p>
              <pre>{{ pretty(execution.resultJson) }}</pre>
            </article>
          </div>
        </section>

        <section class="card">
          <div class="section-head">
            <h2>自动化任务</h2>
            <span class="count">{{ automations.length }} 条</span>
          </div>
          <div class="stack">
            <article v-for="automation in automations" :key="automation.id" class="panel">
              <div class="panel-top">
                <h3>{{ automation.name }}</h3>
                <span class="badge warn">{{ automation.enabled ? '启用中' : '已停用' }}</span>
              </div>
              <p>任务 ID：{{ automation.taskId }}</p>
              <p>周期：{{ automation.intervalMinutes }} 分钟</p>
              <p>创建时间：{{ automation.createdAt }}</p>
            </article>
          </div>
        </section>
      </section>
    </main>
  </div>
</template>
