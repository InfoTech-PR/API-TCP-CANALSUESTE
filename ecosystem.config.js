// LINUX
// module.exports = {
//   apps: [{
//     name: 'API-CANALSUESTE',
//     script: 'gunicorn',
//     args: 'run:app -w 4 -b 0.0.0.0:3002',
//     interpreter: '/usr/bin/python3',
//     instances: 1,
//     exec_mode: 'fork',
//     env: {
//       FLASK_ENV: 'production',
//       PORT: 3002
//     },
//   }]
// };

// WINDOWS
module.exports = {
  apps: [{
    name: 'API-CANALSUESTE',
    script: 'python',
    args: 'run.py', 
    instances: 1,
    exec_mode: 'fork',
    env: {
      FLASK_ENV: 'production',
      PORT: 3002
    },
  }]
};