## Caso queira printar as rotas, use o código abaixo no inicializador logo após iniciar o banco de dados.

```python
for rule in app.url_map.iter_rules(): #? If you want to PRINT the routes
     print(f"Endpoint: {rule.endpoint}, Methods: {', '.join(rule.methods)}, Path: {rule.rule}")```