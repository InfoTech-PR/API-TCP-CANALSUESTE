import soap from 'soap';
import dotenv from 'dotenv';

dotenv.config();

const url = 'https://wsc-hom.tcp.com.br/services/WebservicesClientes_ConsultaPublica?wsdl';

export const getNavioData = (navio: string, status: string, dataInicio: string, dataFinal: string) => {
  return new Promise((resolve, reject) => {
    soap.createClient(url, (err, client: any) => {
      if (err) {
        reject('Erro ao criar cliente SOAP: ' + err);
        return;
      }

      const authHeader = {
        Username: process.env.USER,
        Password: process.env.PASSWORD,
      };

      client.addSoapHeader(authHeader);

      const requestParams = {
        Navio: navio,
        Status: status,
        DataInicio: dataInicio,
        DataFinal: dataFinal,
      };

      client.ConsultaNavio(requestParams, (err: any, result: any) => {
        if (err) {
          reject('Erro na requisição SOAP: ' + err);
        } else {
          resolve(result);
        }
      });
    });
  });
};
