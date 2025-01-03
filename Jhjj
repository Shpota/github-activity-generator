name: Windows Cloud PC - Anydesk (Optimized)

on:
  workflow_dispatch:

jobs:
  build:
    name: Start Building...
    runs-on: windows-latest
    timeout-minutes: 10080  # Máximo de 7 dias para evitar tempo de execução excessivo

    steps:
      - name: Downloading & Installing Essentials
        run: |
          # Baixa o arquivo .bat para instalar componentes essenciais
          Invoke-WebRequest -Uri "https://www.dropbox.com/scl/fi/7eiczvgil84czu55dxep3/Downloads.bat?rlkey=wzdc1wxjsph2b7r0atplmdz3p&dl=1" -OutFile "Downloads.bat"
          # Executa o script .bat para instalar os componentes
          cmd /c Downloads.bat

      - name: Log In To AnyDesk
        run: |
          # Verifica se o arquivo start.bat existe antes de executar
          if (Test-Path "start.bat") {
            cmd /c start.bat
          } else {
            Write-Host "Arquivo start.bat não encontrado. Verifique a configuração."
          }

      - name: Monitor and Restart AnyDesk if Needed
        run: |
          # Monitora a conexão do AnyDesk e reinicia se necessário
          while ($true) {
            $process = Get-Process -Name "AnyDesk" -ErrorAction SilentlyContinue
            if (-not $process) {
              Write-Host "AnyDesk não está rodando, reiniciando..."
              cmd /c start.bat
            }
            Start-Sleep -Seconds 300  # Verifica a cada 5 minutos
          }

      - name: Time Counter (Long Running Task)
        run: |
          # Configura para manter a máquina em execução
          Start-Sleep -Seconds 604800  # 7 dias de execução contínua

      - name: Clean Up Temporary Files
        if: success()  # Executa esta etapa apenas se todas as etapas anteriores forem bem-sucedidas
        run: |
          # Remove arquivos temporários ou logs gerados
          Remove-Item Downloads.bat -Force
          Write-Host "Limpeza completa."
