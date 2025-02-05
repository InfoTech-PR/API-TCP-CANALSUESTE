module.exports = {
  apps: [{
    name: 'flask-api',
    script: 'app.py',  
    instances: 4,  
    exec_mode: 'cluster',  
    env: {
      FLASK_ENV: 'production',
      PORT: 3002
    },
  }]
};
