# ⚡ VectorCalc Pro 2026

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-00D9FF?style=for-the-badge)
![Status](https://img.shields.io/badge/Estado-Terminado-34D399?style=for-the-badge)
![License](https://img.shields.io/badge/Licencia-MIT-7C3AED?style=for-the-badge)

**Sistema Avanzado de Cálculo Integral y Visualización 3D** *Proyecto Terminal - Análisis Vectorial - ESCOM IPN*

[Reportar Bug](https://github.com/TulitasRachet/ProyectoVectorialV2/issues) · [Ver Demo Online](https://tulitasrachet.github.io/ProyectoVectorialV2/)

</div>

---

## 📄 Descripción

**VectorCalc Pro 2026** es una herramienta de software diseñada para estudiantes e ingenieros que buscan precisión y velocidad en el cálculo de integrales múltiples.

El sistema implementa una arquitectura de **Doble Verificación**: calcula simultáneamente la solución exacta (simbólica) y una aproximación numérica (Sumas de Riemann), permitiendo validar la convergencia de los resultados y detectar errores en tiempo real.

---

## 🗂️ Estructura del Repositorio

Este proyecto está organizado en tres módulos principales. Haz clic en las carpetas para acceder al contenido:

### [📂 `Codigo+files`](./Codigo+files)
> **El Núcleo del Proyecto.** Aquí encontrarás el código fuente en Python (`.py`), la lógica matemática (Backend), la interfaz gráfica (Frontend) y los recursos visuales (iconos) necesarios para ejecutar la aplicación de escritorio.

### [📂 `Presentacion-HTML`](./Presentacion-HTML)
> **La Experiencia Web.** Contiene el código fuente de la presentación interactiva.
> * **[Ver Presentación en Vivo 🌐](https://tulitasrachet.github.io/ProyectoVectorialV2/)**

### [📂 `Reporte`](./Reporte)
> **Documentación Técnica.** Aquí se aloja el reporte formal en formato PDF y los archivos fuente en LaTeX (`.tex`) que detallan la justificación teórica, arquitectura y pruebas del sistema.

---

## ✨ Características Principales

* **🧮 Integración Múltiple:** Resolución de integrales dobles ($\iint$) y triples ($\iiint$).
* **🌐 Sistemas de Coordenadas:** Transformación automática con inyección de **Jacobianos**:
    * Cartesianas $(x, y, z)$
    * Cilíndricas $(r, \theta, z)$
    * Esféricas $(\rho, \phi, \theta)$
* **🎨 Visualización 3D:** Motor gráfico integrado para visualizar superficies, contornos y campos vectoriales.
* **⚡ Feedback en Tiempo Real:** Renderizado de ecuaciones en formato $\LaTeX$ mientras escribes.

---

## 🚀 Instalación y Uso

Sigue estos pasos para ejecutar la aplicación de escritorio en tu máquina local.

1.  **Clonar el repositorio**
    ```bash
    git clone [https://github.com/TulitasRachet/VectorCalc-Pro-2026.git](https://github.com/TulitasRachet/VectorCalc-Pro-2026.git)
    cd VectorCalc-Pro-2026
    ```

2.  **Instalar dependencias**
    ```bash
    pip install customtkinter numpy sympy matplotlib pillow
    ```

3.  **Ejecutar la aplicación**
    *(Asegúrate de entrar a la carpeta del código primero)*
    ```bash
    cd Codigo+files
    python "CODIGO FINAL.py"
    ```

---

## 👥 Autores

Este proyecto fue desarrollado con dedicación por estudiantes de la **Escuela Superior de Cómputo (ESCOM)** del **IPN**:

* **Bonilla Hernández Ximena Sofía**
* **Castillo Vidal Carmen Andrea**
* **Cruz Rodríguez Bruno Aarón**

---

<div align="center">
    
**Materia:** Análisis Vectorial (Grupo 26-1)  
**Profesor:** Dr. David Correa Coyac  
    
---
    
*"Este proyecto fue desarrollado con mucho amor*💕 

</div>