# ✏️ EDITA ESTO con tus datos
USERNAME = "Imandro"        # tu usuario de GitHub (el repo debe llamarse igual)
HANDLE   = "imandro"        # lo que sale en el prompt: imandro@github ~ $

# Filas de la tarjeta neofetch: (clave, valor)
INFO = [
    ("Nombre",    "Mario A. Ruiz Alvarez"),
    ("Rol",       "Estudiante · UNAN-León · Equipo DataStorm"),
    ("Enfoque",   "Ciberseguridad · DevOps · Desarrollo de software"),
    ("Stack",     "Python · React · TypeScript · Dart · PostgreSQL"),
    ("Móvil",     "Capacitor · Android nativo · PWA offline-first"),
    ("Proyectos", "AliviaApp · duAI · ConectaMas"),
    ("Desde",     "Nicaragua · trabajando desde casa"),
]

# Banner ASCII (letras disponibles: I M A N D R O S E C U T Y B P V L)
BANNER_NAME = "IMANDRO"
BANNER_LINES = [
    ("$ whoami",  "imandro :: ciberseguridad · devops · desarrollo de software"),
    ("$ cat slogan.txt", "Construye. Despliega. Protege. Repite."),
]

# Proyectos destacados (sección ls projects/)
PROJECTS = [
    ("AliviaApp", "Refugio digital de bienestar mental para jóvenes: respiración guiada, diario terapéutico y SOS en crisis. PWA + app Android nativa, offline-first.",
     "React · TypeScript · Capacitor · PostgreSQL · Vercel"),
    ("duAI", "Herramienta de privacidad para Windows que detecta y elimina todo rastro de uso de IA. 100% local, sin telemetría ni cuentas.",
     "Python · Privacidad · Windows"),
    ("ConectaMas", "Conecta+",
     "TypeScript"),
]

# 🏆 Logros
AWARDS_COUNT = 12
AWARDS_LABEL = ["CONCURSOS", "TECNOLÓGICOS & SOFTWARE"]

# 🧰 Tecnologías (edita libremente): categoría -> lista
TECH = {
    "lenguajes":      ["Python", "TypeScript", "JavaScript", "Dart", "SQL", "HTML/CSS"],
    "frontend/móvil": ["React", "Vite", "Capacitor", "PWA", "Android nativo", "Offline-first"],
    "backend/datos":  ["Node.js", "APIs REST", "PostgreSQL", "Neon", "MySQL", "SQL Server"],
    "devops":         ["AWS", "Git", "GitHub Actions", "CI/CD", "Vercel", "Gradle", "Releases firmados"],
    "ciberseguridad": ["Seguridad de apps", "Autenticación (scrypt)", "Privacidad por diseño", "Bloqueo biométrico"],
}

# ⭐ Proyectos destacados con detalle (los demás repos se leen solos de la API)
FEATURED = [
    dict(name="AliviaApp", tag="v1.2.0 · MIT · Equipo DataStorm",
         desc="Refugio digital de bienestar mental para jóvenes: respiración guiada, diario terapéutico y SOS en crisis.",
         points=["PWA + app Android nativa con un solo código, offline-first (caché + cola FIFO)",
                 "Privacidad: bloqueo biométrico, difuminado al cambiar de app, exportación de datos",
                 "VIA, chat con IA empática · 13 tests del motor offline · base ES/EN"],
         stack=["React", "TypeScript", "Capacitor", "PostgreSQL", "Vercel"]),
    dict(name="duAI", tag="Windows · 100% local",
         desc="Herramienta de privacidad que detecta y elimina todo rastro de uso de IA. Sin telemetría ni cuentas.",
         points=[], stack=["Python", "Privacidad", "Windows"]),
    dict(name="ConectaMas", tag="Conecta+", desc="", points=[], stack=["TypeScript"]),
]
OTHER_MAX = 8

# 📝 Sobre mí (cada elemento = un párrafo)
ABOUT = [
    "Hola, soy Mario 👋 Desde Nicaragua construyo software que protege a las personas: apps que funcionan sin internet, cuidan tus datos y llegan a producción sin drama.",
    "Vivo en la intersección de tres cosas: desarrollo de software, ciberseguridad y DevOps, con AWS como mi casa en la nube. Me obsesiona automatizar lo repetitivo y blindar lo importante.",
    "He ganado 12 concursos tecnológicos y de software, y con DataStorm creé AliviaApp, un refugio digital de bienestar mental para jóvenes. Si quieres colaborar, retarme o hablar de código, escríbeme.",
]
