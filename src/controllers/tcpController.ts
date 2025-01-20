import { Request, Response } from 'express';
import soap from 'soap';
import dotenv from 'dotenv';

dotenv.config();

const url = 'https://wsc-hom.tcp.com.br/services/WebservicesClientes_ConsultaPublica?wsdl';

export const consultaNavioController = (req: Request, res: Response) => {
  const { navio, dataInicio, dataFinal, status } = req.body;

  const requestParams = {
    Navio: navio,
    Status: status || '', 
    DataInicio: dataInicio,
    DataFinal: dataFinal
  };

  soap.createClient(url, (err, client: any) => {
    if (err) {
      console.error('Erro ao criar o cliente SOAP:', err);
      return res.status(500).json({ message: 'Erro interno ao conectar ao serviço SOAP', error: err });
    }

    const authHeader = {
      Username: process.env.USER,
      Password: process.env.PASSWORD
    };

    client.addSoapHeader(authHeader);

    client.ConsultaNavio(requestParams, (err: any, result: any) => {
      if (err) {
        console.error('Erro na requisição SOAP:', err);
        return res.status(500).json({ message: 'Erro ao fazer a requisição SOAP', error: err });
      }
      console.log('Resultado da requisição SOAP:', result);

      return res.status(200).json(result);
    });
  });
};
