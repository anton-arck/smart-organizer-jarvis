from setuptools import setup, find_packages

setup(
    name="smart-organizer-jarvis",
    version="1.5.0",
    author="anton-arck",
    description="Asistente inteligente de organización de archivos con interfaz Cyberpunk",
    packages=find_packages(),
    install_requires=[
        "flet>=0.82.0",
        "watchdog>=6.0.0",
    ],
    python_requires=">=3.12", # Basado en tus librerías actuales
    entry_points={
        'console_scripts': [
            'jarvis-start=main:main', # Esto permite lanzar la app escribiendo 'jarvis-start'
        ],
    },
)
