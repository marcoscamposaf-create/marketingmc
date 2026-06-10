# Como rodar MC Associados no Windows

## 1. Baixar os arquivos

Baixe todos os 9 arquivos desta pasta:
- index.html
- formulario.html
- dashboard.html
- relatorio.html
- style.css
- script.js
- supabase.js
- database.sql
- README.md

Coloque **todos em uma mesma pasta** no seu computador. Ex: `C:\Projetos\mc-associados`

## 2. Abrir PowerShell ou CMD

Abra o **PowerShell** (Windows 10+) ou **Prompt de Comando** (cmd).

## 3. Navegar até a pasta

```powershell
cd C:\Projetos\mc-associados
```

Substitua `C:\Projetos\mc-associados` pelo caminho real onde você salvou os arquivos.

Para confirmar que está no lugar certo, digite:
```powershell
dir
```

Você deve ver os 9 arquivos listados (index.html, style.css, etc.).

## 4. Iniciar o servidor local

Se você tem **Python 3 instalado**:
```powershell
python3 -m http.server 8080
```

Ou, se a versão é Python 2:
```powershell
python -m http.server 8080
```

Você verá algo como:
```
Serving HTTP on 0.0.0.0 port 8080 (http://0.0.0.0:8080/) ...
```

## 5. Abrir o navegador

Abra o navegador e vá para:
```
http://localhost:8080
```

Você verá a página inicial (index.html) com o logo MC Associados, o hero e tudo pronto.

## Troubleshooting

**"python3: comando não encontrado"** ou **"python não é reconhecido"**
- Python não está instalado ou não está no PATH.
- Baixe em https://www.python.org/downloads/
- Certifique-se de marcar a opção "Add Python to PATH" na instalação.

**"Porta 8080 já está em uso"**
- Use outra porta:
```powershell
python3 -m http.server 9000
```
Depois acesse `http://localhost:9000`

**"Permissão negada"**
- Execute o PowerShell como administrador.

---

## Sem Python? Use Node.js

Se preferir, instale Node.js (https://nodejs.org) e use:
```powershell
npx serve .
```

Ou no VS Code: instale a extensão **Live Server** e clique "Open with Live Server".

---

## Modo de operação padrão (LocalStorage)

Assim que você abrir a aplicação, ela já funciona em **modo local** — as respostas
são salvas no localStorage do navegador. Ideal para demonstrar aos sócios.

Para usar um banco de dados real (Supabase), veja as instruções no README.md.
