const http = require('http');
const url = require('url');
const client = require('prom-client');

const register = new client.Registry();

register.setDefaultLabels({
  app: 'metric-demo'
});
client.collectDefaultMetrics({ register });

// Custom metrics
const requestCount = new client.Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status']
});

const requestDuration = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duration of HTTP requests in seconds',
  labelNames: ['method', 'route', 'status'],
  buckets: [0.1, 0.5, 1, 2, 5]
});

register.registerMetric(requestCount);
register.registerMetric(requestDuration);

// Handlers
const server = http.createServer(async (req, res) => {
  const route = url.parse(req.url).pathname;
  const method = req.method;
  const end = requestDuration.startTimer({ method, route });

  if (route === '/metrics') {
    res.setHeader('Content-Type', register.contentType);
    res.end(await register.metrics());
    return;
  }

  if (route === '/fail') {
    requestCount.inc({ method, route, status: 500 });
    res.writeHead(500);
    res.end('Error occurred');
    end({ status: 500 });
    return;
  }

  // Default: success
  requestCount.inc({ method, route, status: 200 });
  res.writeHead(200);
  res.end('Hello from metric app');
  end({ status: 200 });
});

server.listen(8080, () => {
  console.log('🚀 App listening on http://localhost:8080');
});
