# ✏️ EDITA ESTO con tus datos
USERNAME = "Imandro"        # tu usuario de GitHub (el repo debe llamarse igual)
HANDLE   = "imandro"        # lo que sale en el prompt: imandro@github ~ $

# Filas de la tarjeta neofetch: (clave, valor)
INFO = [
    ("Nombre",    "Mario A. Ruiz Alvarez"),
    ("Rol",       "Estudiante · UNAN-León · Equipo DataStorm"),
    ("Enfoque",   "Ciberseguridad · DevOps · Desarrollo de software"),
    ("Stack",     "Python · React · TypeScript · Rust · PostgreSQL"),
    ("Desde",     "Nicaragua · UTC-6"),
]

# Banner ASCII (letras disponibles: I M A N D R O S E C U T Y B P V L)
BANNER_NAME = "IMANDRO"
BANNER_LINES = [
    ("$ whoami",  "imandro :: ciberseguridad · devops · desarrollo de software"),
    ("$ cat slogan.txt", "Construye. Despliega. Protege. Repite."),
]

# Proyectos destacados (referencia para el README)
PROJECTS = [
    ("AliviaApp", "Refugio digital de bienestar mental para jóvenes: PWA, Android e iOS desde un solo código, 100 % offline y privacidad por diseño.",
     "React · TypeScript · Capacitor · PostgreSQL · Azure"),
    ("duAI", "Herramienta de privacidad para Windows que detecta y elimina todo rastro de uso de IA. 100 % local, sin telemetría ni cuentas.",
     "Python · Privacidad · Windows"),
    ("ConectaMas", "Conecta+ — plataforma con 2 000 usuarios en Latinoamérica.",
     "TypeScript"),
    ("NanoAgent", "Agente de IA autónomo para programación, escrito en Rust y optimizado para equipos con pocos recursos.",
     "Rust · IA · CLI"),
]

# 🏆 Logros
AWARDS_COUNT = 12
AWARDS_LABEL = ["concursos tecnológicos", "y de software ganados"]

# 🧰 Tecnologías (referencia para el README): categoría -> lista
TECH = {
    "lenguajes":      ["Python", "TypeScript", "JavaScript", "Dart", "Rust", "SQL"],
    "frontend/móvil": ["React", "Vite", "Capacitor", "PWA", "Android nativo", "Offline-first"],
    "backend/datos":  ["Node.js", "APIs REST", "PostgreSQL", "Neon", "MySQL", "SQL Server"],
    "devops":         ["AWS", "Azure", "Git", "GitHub Actions", "CI/CD", "Vercel", "Gradle"],
    "ciberseguridad": ["Seguridad de apps", "Autenticación (scrypt)", "Privacidad por diseño", "Bloqueo biométrico"],
}

# ⭐ Proyectos destacados con detalle
FEATURED = [
    dict(name="AliviaApp", tag="v1.2.0 · MIT · Equipo DataStorm",
         desc="Refugio digital de bienestar mental para jóvenes: respiración guiada, diario terapéutico y SOS en crisis.",
         points=["PWA + app Android nativa con un solo código, offline-first (caché + cola FIFO)",
                 "Privacidad: bloqueo biométrico, difuminado al cambiar de app, exportación de datos",
                 "Livi, chat con IA empática · 141 tests · base ES/EN"],
         stack=["React", "TypeScript", "Capacitor", "PostgreSQL", "Azure"]),
    dict(name="duAI", tag="Windows · 100% local",
         desc="Herramienta de privacidad que detecta y elimina todo rastro de uso de IA. Sin telemetría ni cuentas.",
         points=[], stack=["Python", "Privacidad", "Windows"]),
    dict(name="ConectaMas", tag="Conecta+ · 2 000 usuarios",
         desc="Plataforma de conexión para estudiantes de Latinoamérica.", points=[], stack=["TypeScript"]),
    dict(name="NanoAgent", tag="Rust · IA local",
         desc="Agente de IA autónomo para programación, optimizado para equipos con pocos recursos.",
         points=[], stack=["Rust", "IA", "CLI"]),
]
OTHER_MAX = 8

# 📝 Sobre mí (cada elemento = un párrafo)
ABOUT = [
    "Hola, soy Mario. Desde Nicaragua construyo software que protege a las personas: apps que funcionan sin internet, cuidan tus datos y llegan a producción sin drama.",
    "Vivo en la intersección de tres cosas: desarrollo de software, ciberseguridad y DevOps, con AWS y Azure como casa en la nube. Me obsesiona automatizar lo repetitivo y blindar lo importante.",
    "He ganado 12 concursos tecnológicos y de software, y con DataStorm creé AliviaApp, un refugio digital de bienestar mental para jóvenes. Si quieres colaborar, retarme o hablar de código, escríbeme.",
]
