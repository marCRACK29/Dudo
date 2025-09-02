# Proyecto TDD: Dudo 

## Integrantes
- Vicente Ramírez
- Carlos Alvarez
- Marcos Martínez

## Instrucciones de uso
Para la correcta ejecución de este proyecto se recomienda utilizar **Python 3.10**.  

### Instalación de dependencias
Ejecuta el siguiente comando para instalar las librerías asociadas con este proyecto:

```bash
pip install -r requirements.txt
```

### Ejecución de tests
Para ejecutar los tests, incluidos los tests de cobertura por archivo, utiliza:

```bash
pytest --cov=src --cov-report=term-missing
```

## Github Actions
Los tests se ejecutan directamente en **GitHub Actions**, lo que asegura que el proceso de integración continua sea automático y replicable en cada push.  
Dentro del workflow, en el apartado **"test with pytest"**, se puede ver el detalle completo de la ejecución de los tests, incluyendo los reportes de cobertura por archivo.

## Sistema operativo
Todo este proyecto fue desarrollado en **Windows**, aunque los tests en GitHub Actions corren en **Linux**, por lo que no debería haber problemas de compatibilidad de nuestro código.
