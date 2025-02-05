module.exports = {
  apps: [{
    name: 'API-CANALSUESTE',
    script: 'gunicorn', 
    args: '-w 4 -b 0.0.0.0:3002 run:app', 
    interpreter: '/usr/local/bin/python3',
    instances: 1,  
    exec_mode: 'fork',  
    env: {
      FLASK_ENV: 'production',
      PORT: 3002
    },
  }]
};
