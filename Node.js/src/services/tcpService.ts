import { Request, Response } from 'express';
import soap from 'soap';
import dotenv from 'dotenv';

dotenv.config();

const url = 'https://wsc-hom.tcp.com.br/services/WebservicesClientes_ConsultaPublica.WebservicesClientes_ConsultaPublicaHttpsSoap12Endpoint?wsdl';

export const consultaNavio = async (
  navio: string,
  dataInicio: string,
  dataFinal: string,
  status: string
): Promise<any> => {
  const requestParams = {
    Navio: navio,
    Status: status || '',
    DataInicio: dataInicio,
    DataFinal: dataFinal,
  };

  try {
    const client = await soap.createClientAsync(url);

    const authHeader = {
      Username: process.env.USER,
      Password: process.env.PASSWORD,
    };

    client.addSoapHeader(authHeader);

    const [result] = await client.ConsultaNavioAsync(requestParams);

    return result;
  } catch (error) {
    if (error instanceof Error) {
      throw new Error(`Erro ao realizar consulta SOAP: ${error.message}`);
    } else {
      throw new Error('Erro desconhecido ao realizar consulta SOAP');
    }
  }
};