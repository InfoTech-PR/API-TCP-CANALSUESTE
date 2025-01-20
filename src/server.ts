import express from 'express';
import bodyParser from 'body-parser';
import { consultaNavioController } from './controllers/tcpController';

const app = express();
const port = 3000;

app.use(bodyParser.json());

app.post('/consulta-navio', consultaNavioController);

app.listen(port, () => {
  console.log(`Servidor rodando em http://localhost:${port}`);
});
