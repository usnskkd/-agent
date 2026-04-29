async function fetchJSON(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || "Request failed");
  }
  return response.json();
}

function formatJson(data) {
  return JSON.stringify(data, null, 2);
}

async function loadTasks() {
  const tasks = await fetchJSON("/api/tasks");
  const target = document.getElementById("taskList");
  target.innerHTML = "";

  if (!tasks.length) {
    target.innerHTML = '<div class="item"><p>暂无任务</p></div>';
    return;
  }

  tasks.forEach((task) => {
    const el = document.createElement("div");
    el.className = "item";
    el.innerHTML = `
      <h3>${task.name}</h3>
      <p><span class="chip">${task.channel}</span></p>
      <p>目标：${task.goal}</p>
      <p>人群：${task.audience}</p>
      <p>预算：${task.budget}</p>
      <div class="row-actions">
        <button data-run="${task.id}">立即执行</button>
        <button data-auto="${task.id}" class="ghost-btn">每60分钟自动执行</button>
      </div>
    `;
    target.appendChild(el);
  });

  document.querySelectorAll("[data-run]").forEach((button) => {
    button.addEventListener("click", async () => {
      await fetchJSON(`/api/tasks/${button.dataset.run}/run`, { method: "POST" });
      await loadExecutions();
    });
  });

  document.querySelectorAll("[data-auto]").forEach((button) => {
    button.addEventListener("click", async () => {
      await fetchJSON("/api/automations", {
        method: "POST",
        body: JSON.stringify({
          task_id: Number(button.dataset.auto),
          name: `Task ${button.dataset.auto} Automation`,
          interval_minutes: 60,
          enabled: true,
        }),
      });
      alert("已创建自动化任务");
    });
  });
}

async function loadExecutions() {
  const executions = await fetchJSON("/api/executions");
  const target = document.getElementById("executionList");
  target.innerHTML = "";

  if (!executions.length) {
    target.innerHTML = '<div class="item"><p>暂无执行记录</p></div>';
    return;
  }

  executions.forEach((execution) => {
    const el = document.createElement("div");
    el.className = "item";
    el.innerHTML = `
      <h3>执行 #${execution.id}</h3>
      <p>任务 ID：${execution.task_id}</p>
      <p>状态：${execution.status}</p>
      <pre>${formatJson(execution.result)}</pre>
    `;
    target.appendChild(el);
  });
}

document.getElementById("taskForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(event.target);
  const payload = Object.fromEntries(formData.entries());
  payload.metadata = {};
  await fetchJSON("/api/tasks", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  event.target.reset();
  await loadTasks();
});

document.getElementById("refreshBtn").addEventListener("click", async () => {
  await Promise.all([loadTasks(), loadExecutions()]);
});

Promise.all([loadTasks(), loadExecutions()]);
