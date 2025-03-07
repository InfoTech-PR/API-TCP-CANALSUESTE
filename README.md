# API-CANALSUESTE
Api desenvolvida para coleta de dados fornecidos pela TCP, e usado em banco próprio para fins de serviço.

# QA - aplicado

- [X] *Testes Unitários*                 {usado o SOAPUI, para simular respostas e ver o tratamento de forma correta}                
- [X] *Testes de Integração*             {usado o SOAPUI, para enviar requisição reais ao endpoint e verificar se resposta esta no formato correto}
- [X] *Testes Funcionais*                {usado o POSTMAN, para simular fluxos complexots e verificar respostas com dados corretos}
- [X] *Testes de Carga e Desempenho*     {usado o LOCUST, onde pude simular 100 usuarios simultaneos chamando os endpoints}
- [X] *Testes de Segurança*              {usado o OWASP ZAP, foi feito por padrão ataques a API, onde trouxe resultados de riscos baixos}
- [X] *CI/CD e Automação*                {usado o Github ACTIONS, foi feito um arquivo de teste para as rotas e a cada commit, o github se encarrega de testar as rotas}