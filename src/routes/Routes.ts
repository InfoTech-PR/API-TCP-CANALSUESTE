import { Router } from 'express';
import { consultaNavioController } from '../controllers/tcpController';

const router = Router();

router.post('/consulta-navio', consultaNavioController);

export default router;
