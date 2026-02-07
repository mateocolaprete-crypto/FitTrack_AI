🚀 FitTrack AI: Tu Asistente Fitness Inteligente
FitTrack AI es una aplicación web de alto rendimiento diseñada para centralizar el control de salud física, nutrición y entrenamiento en una sola plataforma. Utilizando la potencia de la Inteligencia Artificial (Gemini 1.5 Flash), la app elimina la fricción de contar calorías manualmente, permitiendo el registro mediante lenguaje natural.

🌟 Características Principales
📊 Dashboard Inteligente: Visualización en tiempo real de calorías restantes, progreso de macronutrientes y cumplimiento de metas diarias.

🍎 Analizador de Comidas con IA: Gracias a la integración con Google Gemini, el usuario solo describe lo que comió y la IA desglosa automáticamente Calorías, Proteínas, Carbohidratos y Grasas.

💪 Registro de Entrenamiento: Seguimiento de cargas (Progressive Overload) con cálculo automático de volumen total por sesión.

⚙️ Calculadora Científica de Metas: Implementación de la fórmula Mifflin-St Jeor para calcular el TDEE (Gasto Energético Total) según el perfil biométrico y objetivo del usuario.

🛠️ Stack Tecnológico
Frontend: Streamlit (Framework de Python para interfaces de datos).

Cerebro de IA: Google Gemini API (Modelo 1.5 Flash).

Base de Datos: Google Sheets API (Persistencia de datos en la nube).

📂 Estructura del Proyecto
fittrack-ai: 📊_Home.py (Panel central y métricas diarias). requirements.txt  (Dependencias del sistema). pages/ (Módulos de la aplicación):
 🍎_Nutricion.py (Procesamiento de lenguaje natural con IA). 💪_Entrenamiento.py (Log de fuerza y volumen). ⚙️_Configuracion.py (Gestión de perfil y algoritmos de salud)

Lenguaje: Python 3.9+.
