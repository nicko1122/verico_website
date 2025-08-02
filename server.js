const fastify = require('fastify')({ logger: true });
const path = require('path');

// 註冊靜態文件插件
fastify.register(require('@fastify/static'), {
  root: path.join(__dirname, 'static'),
  prefix: '/'
});

// 健康檢查端點
fastify.get('/health', async (request, reply) => {
  return { status: 'ok', timestamp: new Date().toISOString() };
});

// 啟動服務器
const start = async () => {
  try {
    await fastify.listen({ 
      port: 8080, 
      host: '0.0.0.0'  // 監聽所有網路介面
    });
    console.log('🚀 Fastify 服務器已啟動');
    console.log('📍 本地訪問: http://localhost:8080');
    console.log('🌐 遠端訪問: http://192.168.1.135:8080');
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start(); 