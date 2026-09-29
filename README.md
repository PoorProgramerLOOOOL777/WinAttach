🖥️ Windows Shortcut Launcher
Este proyecto es un conjunto de comandos personalizados para Windows 10 y 11, que te permite ejecutar aplicaciones y funciones del sistema mediante combinaciones de teclas simuladas.
Además, incluye una consola interactiva para lanzar programas escribiendo comandos especiales.

🚀 Funcionalidades
Win + A → Abre el Bloc de notas.

Win + C → Abre el Explorador de archivos.

Win + D → Muestra el escritorio.

Win + Ctrl → Abre una consola interactiva donde puedes escribir:

/win/=notepad → abre el Bloc de notas.

/win/=calc → abre la calculadora.

exit → salir de la consola personalizada.

📋 Pasos para usarlo
Abre Notepad en tu PC.

Copia y pega el siguiente código:


Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;
public static class ShortcutKeys {
    [DllImport("user32.dll")]
    public static extern void keybd_event(byte virtualKey, byte scanCode, uint flags, UIntPtr extraInfo);
}
'@

$windowsKey = 0x5B
$keyUp = 0x0002

# Definimos acciones según la tecla secundaria
$actions = @{
    0x41 = { Start-Process "notepad.exe" }   # Win + A → abre Notepad
    0x43 = { Start-Process "explorer.exe" }  # Win + C → abre el Explorador de archivos
    0x44 = {                                # Win + D → mostrar escritorio
        [ShortcutKeys]::keybd_event($windowsKey,0,0,[UIntPtr]::Zero)
        [ShortcutKeys]::keybd_event(0x44,0,0,[UIntPtr]::Zero)
        Start-Sleep -Milliseconds 80
        [ShortcutKeys]::keybd_event(0x44,0,$keyUp,[UIntPtr]::Zero)
        [ShortcutKeys]::keybd_event($windowsKey,0,$keyUp,[UIntPtr]::Zero)
    }
    0x11 = {                                # Win + Ctrl → abrir consola interactiva
        Write-Host "=== Consola personalizada ==="
        Write-Host "Escribe /win/=programa para ejecutar (ej: /win/=notepad)"
        while ($true) {
            $input = Read-Host ">>"
            if ($input -eq "exit") { break }
            elseif ($input -like "/win/=*") {
                $program = $input.Split("=")[1]
                try {
                    Start-Process $program
                    Write-Host "Ejecutando: $program"
                } catch {
                    Write-Host "No se pudo ejecutar: $program"
                }
            } else {
                Write-Host "Comando no reconocido. Usa /win/=programa o 'exit' para salir."
            }
        }
    }
}

# Ejemplo: ejecutar la acción de Win + A
$secondKey = 0x41
if ($actions.ContainsKey($secondKey)) {
    & $actions[$secondKey]
}
Guarda el archivo con extensión .ps1 (por ejemplo: shortcuts.ps1).

Haz clic derecho sobre el archivo y selecciona "Ejecutar con PowerShell".

¡Disfruta de tus nuevos atajos y consola personalizada! 🎉

⚠️ Notas importantes
Este script no reemplaza los atajos originales de Windows, solo añade funciones extra.

Para ejecutar programas ocultos o funciones del sistema, usa la consola con el formato /win/=programa.

Si un programa no se abre, asegúrate de escribir el nombre correcto del ejecutable (ejemplo: explorer.exe, notepad.exe, calc.exe).

Puedes ampliar el hashtable $actions para añadir más combinaciones personalizadas.
