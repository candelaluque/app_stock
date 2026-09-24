# Sistema de Gestión de Stock

Una aplicación web responsiva (PWA) diseñada para el control de stock, registro de ventas y analisis de margenes de ganancia para un comercio local. Desarrollada con un enfoque para ser operada desde dispositivos móviles en el punto de venta.

## Características Principales

*   **Gestión de Stock en Tiempo Real:** Alta de productos con cálculo automatizado de márgenes de ganancia (Precio de Venta vs. Costo).
*   **Punto de Venta Ágil:** Registro de transacciones con descuento automático de inventario.
*   **Reportes Financieros:** Panel de control con métricas de ingresos y ganancias filtradas por semana y mes.
*   **Seguridad:** Sistema de autenticación básica (HTTP Basic Auth) implementado en el backend para restringir accesos no autorizados.
*   **Diseño PWA:** Interfaz optimizada con TailwindCSS, instalable como aplicación nativa en iOS y Android mediante `manifest.json`.

## Stack Tecnológico

*   **Backend:** Python 3, FastAPI, Uvicorn.
*   **Base de Datos:** PostgreSQL (Despliegue) / SQLite (Desarrollo), SQLAlchemy (ORM).
*   **Frontend:** HTML5, Jinja2 (Templating), TailwindCSS.
*   **Despliegue (Deploy):** Render (Web Service), Neon (Serverless Postgres).

## Instalación y Ejecución Local

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/candelaluque/app_stock.git](https://github.com/candelaluque/app_stock.git)
   cd app_stock
