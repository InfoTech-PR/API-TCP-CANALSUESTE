module.exports = {
  apps: [{
    name: 'API-CANALSUESTE',
    script: 'run.py',  
    instances: 1,  
    exec_mode: 'fork',  
    env: {
      FLASK_ENV: 'production',
      PORT: 3002
    },
  }]
};
