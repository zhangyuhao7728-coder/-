#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const { exec } = require('child_process');

const CONFIG_PATH = '/Users/zhangyuhao/.openclaw/openclaw.json';
const PORT = 3000;

// 读取配置
function getConfig() {
  const data = fs.readFileSync(CONFIG_PATH, 'utf8');
  return JSON.parse(data);
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
}

// 获取本地模型列表
function getLocalModels() {
  return new Promise((resolve) => {
    exec('curl -s http://localhost:11434/api/tags', { timeout: 5000 }, (err, stdout) => {
      if (err || !stdout) {
        resolve([]);
        return;
      }
      try {
        const data = JSON.parse(stdout);
        const models = (data.models || []).map(m => ({
          id: `ollama/${m.name}`,
          name: m.name,
          provider: 'ollama',
          type: 'local',
          size: m.size
        }));
        resolve(models);
      } catch {
        resolve([]);
      }
    });
  });
}

// 获取模型列表
async function getModels() {
  const config = getConfig();
  const models = [];
  
  // 云端模型
  if (config.models?.providers) {
    for (const [provider, providerConfig] of Object.entries(config.models.providers)) {
      if (providerConfig.models && provider !== 'ollama') {
        for (const model of providerConfig.models) {
          models.push({
            id: `${provider}/${model.id}`,
            name: model.name || model.id,
            provider: provider,
            type: 'cloud',
            cost: model.cost
          });
        }
      }
    }
  }
  
  // 本地模型
  const localModels = await getLocalModels();
  return [...models, ...localModels];
}

// 获取当前主模型
function getCurrentModel() {
  const config = getConfig();
  return config.agents?.defaults?.model?.primary || 'minimax-cn/MiniMax-M2.5';
}

// 设置主模型
function setPrimaryModel(modelId) {
  const config = getConfig();
  
  if (!config.agents) config.agents = {};
  if (!config.agents.defaults) config.agents.defaults = {};
  if (!config.agents.defaults.model) config.agents.defaults.model = {};
  
  // 判断是云端还是本地模型
  const isLocal = modelId.startsWith('ollama/');
  
  if (isLocal) {
    // 本地模型作为主模型
    config.agents.defaults.model.primary = modelId;
    config.agents.defaults.model.fallbacks = ['minimax-cn/MiniMax-M2.5'];
  } else {
    // 云端模型作为主模型
    config.agents.defaults.model.primary = modelId;
    config.agents.defaults.model.fallbacks = ['ollama/qwen3.5:9b'];
  }
  
  saveConfig(config);
  return true;
}

// 获取 Gateway 状态
function getGatewayStatus() {
  return new Promise((resolve) => {
    exec('curl -s http://localhost:18789/health', { timeout: 3000 }, (err, stdout) => {
      if (err) {
        resolve({ status: 'offline', uptime: 0 });
        return;
      }
      try {
        const data = JSON.parse(stdout);
        resolve({ status: 'online', ...data });
      } catch {
        resolve({ status: 'online' });
      }
    });
  });
}

// 获取模型使用统计
function getModelStats() {
  return new Promise((resolve) => {
    exec('curl -s http://localhost:18789/api/stats', { timeout: 3000 }, (err, stdout) => {
      if (err) {
        resolve(null);
        return;
      }
      try {
        resolve(JSON.parse(stdout));
      } catch {
        resolve(null);
      }
    });
  });
}

// HTML 页面
const HTML = `
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🤖 AI 模型管理中心</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
      min-height: 100vh;
      color: #fff;
      padding: 20px;
    }
    .container { max-width: 900px; margin: 0 auto; }
    
    /* 顶部标题 */
    .header {
      text-align: center;
      margin-bottom: 30px;
    }
    .header h1 { 
      font-size: 2.5em;
      margin-bottom: 10px;
      background: linear-gradient(90deg, #00d4ff, #a855f7, #ec4899);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .header p { color: #888; }
    
    /* 状态栏 */
    .status-bar {
      display: flex;
      gap: 15px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .status-item {
      flex: 1;
      min-width: 150px;
      background: rgba(255,255,255,0.1);
      border-radius: 12px;
      padding: 15px 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      backdrop-filter: blur(10px);
    }
    .status-icon { font-size: 1.5em; }
    .status-info h4 { color: #888; font-size: 0.85em; font-weight: normal; }
    .status-info p { font-weight: bold; font-size: 1.1em; }
    .status-online { color: #10b981; }
    .status-offline { color: #ef4444; }
    
    /* 卡片 */
    .card {
      background: rgba(255,255,255,0.08);
      border-radius: 20px;
      padding: 24px;
      margin-bottom: 20px;
      backdrop-filter: blur(20px);
      border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* 当前模型 */
    .current-model {
      text-align: center;
      padding: 30px;
      background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(168,85,247,0.1));
      border-radius: 16px;
    }
    .current-model .label { color: #888; margin-bottom: 10px; font-size: 0.9em; }
    .current-model .model-name { 
      font-size: 2.2em; 
      font-weight: bold;
      background: linear-gradient(90deg, #00d4ff, #a855f7);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .current-model .model-type {
      display: inline-block;
      margin-top: 10px;
      padding: 6px 16px;
      border-radius: 20px;
      font-size: 0.9em;
    }
    .type-cloud { background: rgba(168,85,247,0.3); color: #a855f7; }
    .type-local { background: rgba(16,185,129,0.3); color: #10b981; }
    
    /* 模型列表 */
    .section-title {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
      font-size: 1.3em;
    }
    .model-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }
    
    .model-card {
      padding: 18px;
      background: rgba(255,255,255,0.05);
      border-radius: 14px;
      cursor: pointer;
      transition: all 0.3s;
      border: 2px solid transparent;
      position: relative;
      overflow: hidden;
    }
    .model-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 3px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
      opacity: 0;
      transition: opacity 0.3s;
    }
    .model-card:hover {
      background: rgba(255,255,255,0.1);
      transform: translateY(-3px);
      box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    .model-card:hover::before { opacity: 1; }
    .model-card.active {
      border-color: #00d4ff;
      background: rgba(0,212,255,0.15);
      box-shadow: 0 0 30px rgba(0,212,255,0.2);
    }
    .model-card-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 10px;
    }
    .model-name-title { font-size: 1.1em; font-weight: bold; }
    .model-provider { color: #666; font-size: 0.85em; }
    .model-id { color: #555; font-size: 0.8em; margin-top: 5px; }
    .model-badge {
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 0.75em;
      font-weight: bold;
    }
    .badge-cloud { background: linear-gradient(135deg, #a855f7, #7c3aed); }
    .badge-local { background: linear-gradient(135deg, #10b981, #059669); }
    
    .model-size {
      margin-top: 10px;
      font-size: 0.8em;
      color: #666;
    }
    
    /* 成本信息 */
    .cost-info {
      display: flex;
      gap: 15px;
      margin-top: 8px;
      font-size: 0.8em;
    }
    .cost-item { color: #888; }
    .cost-value { color: #10b981; font-weight: bold; }
    
    /* 操作按钮 */
    .action-buttons {
      display: flex;
      gap: 10px;
      margin-top: 15px;
    }
    .btn {
      flex: 1;
      padding: 12px 20px;
      border-radius: 10px;
      border: none;
      cursor: pointer;
      font-size: 0.95em;
      transition: all 0.3s;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }
    .btn-primary {
      background: linear-gradient(135deg, #00d4ff, #a855f7);
      color: white;
    }
    .btn-primary:hover { transform: scale(1.02); box-shadow: 0 5px 20px rgba(0,212,255,0.4); }
    .btn-secondary {
      background: rgba(255,255,255,0.1);
      color: white;
    }
    .btn-secondary:hover { background: rgba(255,255,255,0.2); }
    
    /* 状态消息 */
    .status-message { 
      text-align: center; 
      padding: 15px; 
      border-radius: 12px;
      margin-top: 20px;
      display: none;
      font-weight: 500;
    }
    .status-message.show { display: block; }
    .status-message.success { 
      background: rgba(16,185,129,0.2); 
      color: #10b981; 
      border: 1px solid rgba(16,185,129,0.3);
    }
    .status-message.error { 
      background: rgba(239,68,68,0.2); 
      color: #ef4444; 
      border: 1px solid rgba(239,68,68,0.3);
    }
    .status-message.loading { 
      background: rgba(0,212,255,0.2); 
      color: #00d4ff; 
      border: 1px solid rgba(0,212,255,0.3);
    }
    
    /* 分隔线 */
    .divider {
      height: 1px;
      background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
      margin: 20px 0;
    }
    
    /* 刷新按钮 */
    .refresh-btn {
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(255,255,255,0.1);
      border: none;
      color: white;
      padding: 12px 18px;
      border-radius: 12px;
      cursor: pointer;
      font-size: 1em;
      transition: all 0.3s;
    }
    .refresh-btn:hover { background: rgba(255,255,255,0.2); }
  </style>
</head>
<body>
  <button class="refresh-btn" onclick="loadAll()">🔄 刷新</button>
  
  <div class="container">
    <div class="header">
      <h1>🤖 AI 模型管理中心</h1>
      <p>支持云端 & 本地模型 · 一键切换 · 实时生效</p>
    </div>
    
    <!-- 状态栏 -->
    <div class="status-bar">
      <div class="status-item">
        <span class="status-icon">🟢</span>
        <div class="status-info">
          <h4>Gateway 状态</h4>
          <p id="gatewayStatus" class="status-online">在线</p>
        </div>
      </div>
      <div class="status-item">
        <span class="status-icon">📊</span>
        <div class="status-info">
          <h4>可用模型</h4>
          <p id="modelCount">-</p>
        </div>
      </div>
      <div class="status-item">
        <span class="status-icon">☁️</span>
        <div class="status-info">
          <h4>云端模型</h4>
          <p id="cloudCount">-</p>
        </div>
      </div>
      <div class="status-item">
        <span class="status-icon">💻</span>
        <div class="status-info">
          <h4>本地模型</h4>
          <p id="localCount">-</p>
        </div>
      </div>
    </div>
    
    <!-- 当前模型 -->
    <div class="card">
      <div class="current-model">
        <div class="label">✨ 当前使用模型</div>
        <div class="model-name" id="currentModel">加载中...</div>
        <span class="model-type" id="currentType">-</span>
      </div>
    </div>
    
    <!-- 云端模型 -->
    <div class="card">
      <div class="section-title">☁️ 云端模型</div>
      <div class="model-grid" id="cloudModels"></div>
    </div>
    
    <!-- 本地模型 -->
    <div class="card">
      <div class="section-title">💻 本地模型 (Ollama)</div>
      <div class="model-grid" id="localModels"></div>
    </div>
    
    <!-- 操作 -->
    <div class="action-buttons">
      <button class="btn btn-secondary" onclick="restartGateway()">🔁 重启 Gateway</button>
      <button class="btn btn-primary" onclick="openclawDashboard()">🚀 OpenClaw 控制台</button>
    </div>
    
    <div class="status-message" id="statusMessage"></div>
  </div>
  
  <script>
    let allModels = [];
    let currentModel = '';
    
    function formatSize(bytes) {
      const gb = bytes / (1024*1024*1024);
      if (gb >= 1) return gb.toFixed(1) + ' GB';
      const mb = bytes / (1024*1024);
      return mb.toFixed(0) + ' MB';
    }
    
    function showMessage(msg, type) {
      const el = document.getElementById('statusMessage');
      el.textContent = msg;
      el.className = 'status-message show ' + type;
      if (type !== 'loading') {
        setTimeout(() => el.className = 'status-message', 5000);
      }
    }
    
    async function loadAll() {
      showMessage('正在加载...', 'loading');
      
      try {
        const [modelsRes, currentRes, statusRes] = await Promise.all([
          fetch('/api/models'),
          fetch('/api/current'),
          fetch('/api/status')
        ]);
        
        allModels = await modelsRes.json();
        currentModel = await currentRes.json();
        const status = await statusRes.json();
        
        // 更新状态栏
        document.getElementById('gatewayStatus').textContent = status.status === 'online' ? '在线' : '离线';
        document.getElementById('gatewayStatus').className = status.status === 'online' ? 'status-online' : 'status-offline';
        document.getElementById('modelCount').textContent = allModels.length;
        
        const cloudModels = allModels.filter(m => m.type === 'cloud');
        const localModels = allModels.filter(m => m.type === 'local');
        document.getElementById('cloudCount').textContent = cloudModels.length;
        document.getElementById('localCount').textContent = localModels.length;
        
        // 更新当前模型
        document.getElementById('currentModel').textContent = currentModel;
        const currentType = currentModel.startsWith('ollama/') ? 'local' : 'cloud';
        const typeEl = document.getElementById('currentType');
        typeEl.textContent = currentType === 'cloud' ? '☁️ 云端' : '💻 本地';
        typeEl.className = 'model-type ' + (currentType === 'cloud' ? 'type-cloud' : 'type-local');
        
        // 渲染云端模型
        document.getElementById('cloudModels').innerHTML = cloudModels.map(m => \`
          <div class="model-card \${m.id === currentModel ? 'active' : ''}" onclick="switchModel('\${m.id}')">
            <div class="model-card-header">
              <div>
                <div class="model-name-title">\${m.name}</div>
                <div class="model-provider">\${m.provider}</div>
              </div>
              <span class="model-badge badge-cloud">☁️ 云端</span>
            </div>
            <div class="model-id">\${m.id}</div>
            \${m.cost ? \`<div class="cost-info">
              <span class="cost-item">输入: <span class="cost-value">$\{m.cost.input\}</span>/1M</span>
              <span class="cost-item">输出: <span class="cost-value">$\{m.cost.output\}</span>/1M</span>
            </div>\` : ''}
          </div>
        \`).join('<div class="divider"></div>') || '<p style="color:#666;text-align:center;">暂无云端模型</p>';
        
        // 渲染本地模型
        document.getElementById('localModels').innerHTML = localModels.map(m => \`
          <div class="model-card \${m.id === currentModel ? 'active' : ''}" onclick="switchModel('\${m.id}')">
            <div class="model-card-header">
              <div>
                <div class="model-name-title">\${m.name}</div>
                <div class="model-provider">Ollama 本地运行</div>
              </div>
              <span class="model-badge badge-local">💻 本地</span>
            </div>
            <div class="model-id">\${m.id}</div>
            \${m.size ? \`<div class="model-size">📦 \${formatSize(m.size)}</div>\` : ''}
          </div>
        \`) || '<p style="color:#666;text-align:center;">本地无运行中的模型</p>';
        
        showMessage('✅ 加载完成', 'success');
      } catch (e) {
        showMessage('❌ 加载失败: ' + e.message, 'error');
      }
    }
    
    async function switchModel(modelId) {
      if (modelId === currentModel) return;
      
      showMessage('正在切换模型...', 'loading');
      
      try {
        const res = await fetch('/api/set', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({model: modelId})
        });
        const result = await res.json();
        
        if (result.success) {
          const type = modelId.startsWith('ollama/') ? '💻 本地' : '☁️ 云端';
          showMessage('✅ 切换成功！正在重启 Gateway...', 'success');
          currentModel = modelId;
          loadAll();
        } else {
          throw new Error(result.error);
        }
      } catch (e) {
        showMessage('❌ 切换失败: ' + e.message, 'error');
      }
    }
    
    async function restartGateway() {
      showMessage('正在重启 Gateway...', 'loading');
      try {
        await fetch('/api/restart', { method: 'POST' });
        showMessage('✅ Gateway 正在重启，约3秒后生效', 'success');
        setTimeout(loadAll, 4000);
      } catch (e) {
        showMessage('❌ 重启失败: ' + e.message, 'error');
      }
    }
    
    function openclawDashboard() {
      window.open('http://localhost:18789', '_blank');
    }
    
    loadAll();
    
    // 每30秒自动刷新
    setInterval(loadAll, 30000);
  </script>
</body>
</html>
`;

// API 路由
const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }
  
  if (req.url === '/') {
    res.writeHead(200, {'Content-Type': 'text/html;charset=utf-8'});
    res.end(HTML);
    return;
  }
  
  if (req.url === '/api/models') {
    getModels().then(models => {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify(models));
    });
    return;
  }
  
  if (req.url === '/api/current') {
    res.writeHead(200, {'Content-Type': 'application/json'});
    res.end(JSON.stringify(getCurrentModel()));
    return;
  }
  
  if (req.url === '/api/status') {
    getGatewayStatus().then(status => {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify(status));
    });
    return;
  }
  
  if (req.url === '/api/set' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const {model} = JSON.parse(body);
        setPrimaryModel(model);
        res.writeHead(200, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({success: true}));
      } catch (e) {
        res.writeHead(500, {'Content-Type': 'application/json'});
        res.end(JSON.stringify({success: false, error: e.message}));
      }
    });
    return;
  }
  
  if (req.url === '/api/restart' && req.method === 'POST') {
    exec('kill -USR1 $(pgrep -f "openclaw.*gateway")', (err) => {
      res.writeHead(200, {'Content-Type': 'application/json'});
      res.end(JSON.stringify({success: !err}));
    });
    return;
  }
  
  res.writeHead(404);
  res.end('Not Found');
});

server.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           🤖 AI 模型管理界面 v2.0 已启动                      ║
╠═══════════════════════════════════════════════════════════════╣
║  本地访问: http://localhost:${PORT}                               ║
║  功能: ☁️ 云端模型 + 💻 本地模型 + 一键切换                     ║
╚═══════════════════════════════════════════════════════════════╝
  `);
});
