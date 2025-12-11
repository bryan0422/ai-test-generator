#!/usr/bin/env python3
"""
CLI para AI Test Generator
"""

import click
import os
from pathlib import Path
from src.ai_generator import AITestGenerator
from src.validators import CodeValidator

# Banner bonito
BANNER = """
╔═══════════════════════════════════════════╗
║     🤖 AI Test Generator CLI v1.0        ║
║     Generador automático de tests        ║
╚═══════════════════════════════════════════╝
"""


@click.group()
def cli():
    """🤖 AI Test Generator - Genera tests con Claude AI"""
    pass

@cli.command()
@click.argument('user_story', required=False)  # ← Cambio 1: required=False
@click.option('--file', '-f', 'file_path', type=click.Path(exists=True), help='Leer user story desde archivo') 
@click.option('--output', '-o', default='tests', help='Directorio de salida')
@click.option('--filename', 'output_filename', help='Nombre del archivo (auto si no se provee)') 
@click.option('--show-gherkin', '-g', is_flag=True, help='Mostrar Gherkin generado')
def generate(user_story, file_path, output, output_filename, show_gherkin):
    """
    Genera un test de Playwright desde una user story.
    
    Ejemplos:
        python cli.py generate "As a user I want to login"
        python cli.py generate --file user_stories/login.txt
    """
   
    print(BANNER)
    print("🚀 Generando test...")
    print()
    
    # Determinar la user story (desde archivo o argumento)
    if file_path:
        # Leer desde archivo
        try:
            with open(file_path, 'r') as f:
                user_story = f.read()
            click.echo(f"📁 Leyendo desde: {file_path}")
        except Exception as e:
            click.echo(f"❌ Error al leer archivo: {e}", err=True)
            return
    elif not user_story:
        # Si no hay ni archivo ni argumento
        click.echo("❌ Error: Debes proveer una user story o usar --file", err=True)
        click.echo("💡 Ejemplo: python cli.py generate --file user_stories/login.txt")
        click.echo("💡 O: python cli.py generate \"As a user I want...\"")
        return
    # ====== FIN CÓDIGO NUEVO ======
    
    # Crear generador
    try:
        generator = AITestGenerator()
    except ValueError as e:
        click.echo(f"❌ Error: {e}", err=True)
        click.echo("💡 Asegúrate de tener ANTHROPIC_API_KEY en .env")
        return
    
    # Generar test
    click.echo(f"📖 User Story: {user_story[:100]}...")
    click.echo()
    
    with click.progressbar(length=2, label='Generando') as bar:
        result = generator.generate_complete_test(user_story)
        bar.update(2)
    
    # Mostrar Gherkin si se solicita
    if show_gherkin:
        click.echo()
        click.echo("📝 GHERKIN GENERADO:")
        click.echo("─" * 60)
        click.echo(result['gherkin'])
        click.echo()
    
    # Mostrar validación
    validation = result['validation']
    click.echo("🔍 VALIDACIÓN:")
    click.echo("─" * 60)
    
    if validation.is_valid:
        click.secho("✅ Código validado exitosamente", fg='green')
    else:
        click.secho("⚠️  Código tiene problemas", fg='yellow')
    
    # Errores
    if validation.errors:
        click.secho("\n🔴 ERRORES:", fg='red')
        for error in validation.errors:
            click.echo(f"  - {error}")
    
    # Advertencias
    if validation.warnings:
        click.secho("\n⚠️  ADVERTENCIAS:", fg='yellow')
        for warning in validation.warnings:
            click.echo(f"  - {warning}")
    
    # Sugerencias
    if validation.suggestions:
        click.secho("\n💡 SUGERENCIAS:", fg='cyan')
        for suggestion in validation.suggestions:
            click.echo(f"  - {suggestion}")
    
    # Guardar archivo
    click.echo()
    output_dir = Path(output)
    output_dir.mkdir(exist_ok=True)
    
    if not output_filename:
        # Generar nombre automático
        import re
        # Extraer palabras clave de la user story
        words = re.findall(r'\w+', user_story.lower())
        # Tomar las primeras 3-4 palabras significativas
        keywords = [w for w in words if w not in ['as', 'a', 'an', 'i', 'want', 'to', 'the', 'so', 'that']][:3]
        output_filename = f"test_{'_'.join(keywords)}.py"
    
    output_path = output_dir / output_filename
    
    with open(output_path, 'w') as f:
        f.write(result['code'])
    
    click.secho(f"\n✅ Test guardado en: {output_path}", fg='green')
    click.echo()
    click.echo("🎯 Para ejecutar:")
    click.echo(f"   python -m pytest {output_path} -v")
    click.echo()
    
    
@cli.command()
@click.argument('filepath', type=click.Path(exists=True))
def validate(filepath):
    """
    Valida un archivo de test de Playwright.
    
    Ejemplo:
        python cli.py validate tests/test_example.py
    """
    print(BANNER)
    print(f"🔍 Validando: {filepath}")
    print()
    
    # Leer archivo
    try:
        with open(filepath, 'r') as f:
            code = f.read()
    except Exception as e:
        click.echo(f"❌ Error al leer archivo: {e}", err=True)
        return
    
    # Validar
    validator = CodeValidator()
    result = validator.validate_code(code)
    
    # Mostrar resultado
    click.echo("─" * 60)
    
    if result.is_valid:
        click.secho("✅ VALIDACIÓN EXITOSA", fg='green', bold=True)
    else:
        click.secho("❌ VALIDACIÓN FALLIDA", fg='red', bold=True)
    
    # Errores
    if result.errors:
        click.echo()
        click.secho("🔴 ERRORES:", fg='red', bold=True)
        for error in result.errors:
            click.echo(f"  - {error}")
    
    # Advertencias
    if result.warnings:
        click.echo()
        click.secho("⚠️  ADVERTENCIAS:", fg='yellow', bold=True)
        for warning in result.warnings:
            click.echo(f"  - {warning}")
    
    # Sugerencias
    if result.suggestions:
        click.echo()
        click.secho("💡 SUGERENCIAS:", fg='cyan', bold=True)
        for suggestion in result.suggestions:
            click.echo(f"  - {suggestion}")
    
    click.echo()
    click.echo("─" * 60)
    
    # Exit code según validación
    if not result.is_valid:
        raise click.ClickException("Validación fallida")    
    
    
@cli.command()
def info():
    """Muestra información del sistema."""
    print(BANNER)
    
    click.echo("📊 INFORMACIÓN DEL SISTEMA")
    click.echo("─" * 60)
    click.echo(f"Python: {click.__version__}")
    click.echo(f"Proyecto: AI Test Generator v1.0")
    click.echo(f"Directorio: {os.getcwd()}")
    
    # Verificar API key
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        click.secho("✅ API Key configurada", fg='green')
    else:
        click.secho("❌ API Key NO configurada", fg='red')
        click.echo("💡 Configúrala en .env")
    
    # Verificar directorios
    click.echo()
    click.echo("📁 ESTRUCTURA:")
    
    paths = {
        "src/": "Código fuente",
        "tests/": "Tests generados",
        ".env": "Configuración",
    }
    
    for path, desc in paths.items():
        exists = os.path.exists(path)
        icon = "✅" if exists else "❌"
        click.echo(f"  {icon} {path:20} {desc}")
    
    click.echo()    
    
if __name__ == '__main__':
    cli()    