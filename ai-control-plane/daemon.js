/**
 * AI Control Plane - 进程守护脚本
 * 自动监控并重启服务
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const LOG_FILE = path.join(__dirname, 'logs', 'daemon.log');
const PID_FILE = path.join(__dirname, 'daemon.pid');
const SERVER_FILE = path.join(__dirname, 'server.js');

function log(msg) {
  const line = `[${new Date().toISOString()}] ${msg}\n`;
  fs.appendFileSync(LOG_FILE, line);
  console.log(msg);
}

let serverProcess = null;
let restarting = false;

function startServer() {
  if (serverProcess) {
    serverProcess.kill();
  }
  
  log('启动服务...');
  serverProcess = spawn('node', [SERVER_FILE], {
    cwd: __dirname,
    stdio: ['ignore', 'pipe', 'pipe']
  });
  
  serverProcess.stdout.on('data', (data) => {
    process.stdout.write(data);
  });
  
  serverProcess.stderr.on('data', (data) => {
    process.stderr.write(data);
  });
  
  serverProcess.on('exit', (code) => {
    log(`服务退出, code: ${code}`);
    serverProcess = null;
    if (!restarting) {
      log('5秒后自动重启...');
      setTimeout(startServer, 5000);
    }
  });
}

function monitor() {
  // 每30秒检查一次
  setInterval(() => {
    if (!serverProcess || serverProcess.exitCode !== null) {
      log('检测到服务停止，准备重启...');
      startServer();
    }
  }, 30000);
}

function stop() {
  restarting = true;
  if (serverProcess) {
    serverProcess.kill();
  }
  log('守护进程已停止');
  process.exit(0);
}

// 信号处理
process.on('SIGTERM', stop);
process.on('SIGINT', stop);

// 启动
log('========================================');
log('🤖 AI Control Plane 守护进程启动');
log('========================================');
startServer();
monitor();
