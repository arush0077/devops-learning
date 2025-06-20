const http = require('http');
const { Pool } = require('pg');

const pool = new Pool({
  user: process.env.DB_USER || 'myuser',
  host: process.env.DB_HOST || 'host.docker.internal',
  database: process.env.DB_NAME || 'mydatabase',
  password: process.env.DB_PASSWORD || 'mysecretpassword',
  port: parseInt(process.env.DB_PORT || '5432'),
});

const server = http.createServer(async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW() as now');
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ message: 'Connected to PostgreSQL', time: result.rows[0].now }));
  } catch (err) {
    res.writeHead(500, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: err.message }));
  }
});

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
