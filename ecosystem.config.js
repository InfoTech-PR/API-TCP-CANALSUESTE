// module.exports = {
//   apps: [{
//     name: 'API-CANALSUESTE',
//     script: 'C:/Users/Infotech/AppData/Local/Programs/Python/Python312/python.exe',
//     args: 'run.py',
//     instances: 1,
//     exec_mode: 'fork',
//     env: {
//       FLASK_ENV: 'production',
//       PORT: 3002
//     },
//   }]
// };

module.exports = {
  apps: [{
    name: 'API-CANALSUESTE',
    script: 'usr/python3/bin',
    args: 'run.py',
    instances: 1,
    exec_mode: 'fork',
    env: {
      FLASK_ENV: 'production',
      PORT: 3002
    },
  }]
};
