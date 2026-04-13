# Impacto de los valores atípicos e incertidumbre estadística en el análisis del consumo global de alcohol (2015-2019)

## Planteamiento del problema 
El estudio del consumo de alcohol a nivel global es fundamental para entender comportamientos socioeconómicos y de salud pública. Este proyecto utiliza herramientas de computación científica para analizar el dataset `alcohol_data.csv`, enfocándose en la distribución del consumo per cápita y la cuantificación de la incertidumbre en las estimaciones estadísticas.

El análisis global del consumo de alcohol suele caer en el reduccionismo estadístico, presentando promedios nacionales como verdades absolutas. Este proyecto cuestiona dicha práctica, señalando que el promedio es una medida sensible a valores atípicos y sesgos de selección, especialmente en países con sistemas de registro deficientes. La investigación se centra en la incertidumbre estadística y en cómo la omisión de los intervalos de confianza oculta crisis de salud pública detrás de una falsa sensación de precisión.

## Resumen
En el presente informe se realiza un análisis del impacto de los valores atípicos y la incertidumbre estadística en las estimaciones del consumo global de alcohol (2015-2019). Se examina la robustez del promedio frente a la mediana y se evalúa la precisión de los intervalos de confianza mediante el análisis de solapamiento regional, aplicando técnicas de limpieza de datos (ETL), truncamiento por percentiles y visualización de densidades con R.

## Objetivos 
## Objetivo General
Cuestionar la validez de las comparaciones tradicionales del consumo de alcohol a nivel mundial mediante el procesamiento computacional de los intervalos de confianza proporcionados en el dataset, con el fin de evidenciar el solapamiento de datos y la incertidumbre estadística que el promedio suele invisibilizar.
## Objetivos Específicos 

**1.Extraer y depurar** los registros de consumo de alcohol y sus intervalos de confianza, gestionando los valores faltantes y contrastando la media frente a la mediana para identificar el sesgo generado por valores atípicos (outliers) en el promedio.

 **2.Evaluar la variabilidad** en la precisión de las estimaciones analizando el ancho de los márgenes de error para cuestionar la consistencia de los reportes globales
 
**3.Identificar y visualizar** los niveles de solapamiento de los intervalos de confianza, con el fin de determinar regiones donde las diferencias en los promedios carecen de verdad estadística, culminando en la generación de un reporte técnico reproducible que evidencie la incertidumbre de los datos.

## Integrantes
* Andrea Figuera.
* Eduardo Espinoza. 

###### Informe Dinámico con Rmarkdown: [Enlace próximamente]
###### Dashboard con Python: https://siracussa-npsfpqhza3jmzxueunpifr.streamlit.app/

![Static Badge](https://img.shields.io/badge/R-blue) ![Static Badge](https://img.shields.io/badge/Python-yellow) ![Static Badge](https://img.shields.io/badge/UCV-red)
