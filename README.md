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

## 🌿 Organización del Repositorio

Para mantener el proyecto modular, **hemos migrado los recursos a diferentes ramas**.
Selecciona el módulo que deseas consultar para ir directo a su documentación:

| Módulo | Contenido | Branch (Rama) |
| :--- | :--- | :---: |
| **💻 Código Fuente** | Backend, Interfaz Gráfica (`.py`) y Assets. Es el núcleo de la aplicación. | [`📂 Ir a rama Codigo+files`](https://github.com/TulitasRachet/ProyectoVectorialV2/tree/Codigo%2Bfiles) |
| **🌐 Web** | Código fuente de la presentación interactiva HTML. | [`📂 Ir a rama Presentacion-HTML`](https://github.com/TulitasRachet/ProyectoVectorialV2/tree/Presentacion-HTML) |
| **📝 Documentación** | Reporte técnico en PDF y archivos fuente LaTeX (`.tex`). | [`📂 Ir a rama Reporte`](https://github.com/TulitasRachet/ProyectoVectorialV2/tree/Reporte) |

> **Nota:** Al hacer clic en los enlaces, GitHub te llevará a la rama correspondiente y te mostrará el `README` específico de esa sección.

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

Sigue estos pasos para obtener el código y ejecutar la aplicación.

1.  **Clonar el repositorio**
    ```bash
    git clone [https://github.com/TulitasRachet/ProyectoVectorialV2.git](https://github.com/TulitasRachet/ProyectoVectorialV2.git)
    cd ProyectoVectorialV2
    ```

2.  **Cambiar a la rama del código**
    El código fuente principal se encuentra en la rama `Codigo+files`:
    ```bash
    git checkout Codigo+files
    ```

3.  **Instalar dependencias**
    ```bash
    pip install customtkinter numpy sympy matplotlib pillow
    ```

4.  **Ejecutar la aplicación**
    *(Asegúrate de estar en la raíz de la rama descargada)*
    ```bash
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
