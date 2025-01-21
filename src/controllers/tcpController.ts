import { Request, Response } from 'express';
import { consultaNavio } from '../services/tcpService';

export const consultaNavioController = async (req: Request, res: Response) => {
  const { navio, dataInicio, dataFinal, status } = req.body;

  try {
    const result = await consultaNavio(navio, dataInicio, dataFinal, status);
    
    console.log('Resultado da requisição SOAP:', result);
    return res.status(200).json(result);
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : 'Erro desconhecido';
    
    console.error('Erro ao realizar consulta SOAP:', errorMessage);
    
    return res.status(500).json({
      message: 'Erro ao realizar consulta SOAP',
      error: errorMessage
    });
  }
};