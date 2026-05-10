module.exports = {
  apps: [
    {
      name: 'lafiya-backend',
      cwd: '/home/debian/apps/lafiyabackend',
      script: 'venv/bin/python',
      args: '-m uvicorn app.main:app --host 127.0.0.1 --port 4256',
      interpreter: 'none',
      exec_mode: 'fork',
      instances: 1,
      autorestart: true,
      watch: false,
      max_memory_restart: '300M',
      env: {
        PYTHONUNBUFFERED: '1',
        DATABASE_URL: 'sqlite:///./lafiya.db'
      }
    }
  ]
};