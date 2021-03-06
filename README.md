<h2>Instrukcja włączenia projektu</h2>
<p>W terminalu należy przejść do folderu zawierającego projekt</p>
<ul>
  <li>Odpalenie zdokeryzowanej strony typu develop</li>
    <ol>
      <li>W terminalu należy wpisać komendę: "docker pull theripson/djangoproject:web".<br>
      Po wpisaniu pobierane są wszystkie pliki potrzebne do włączenia strony.
      </li>
      <li>Następnie wpisanie komendy: "docker-compose.exe up".<br>
      Należy wpisać w przeglądarce adres: 127.0.0.1:8000</li>
      <li>Należy stworzyć konto administratora komendą: "python .\manage.py createsuperuser". Aby wejść w panel administratora na stronie adres przeglądarki powinien wyglądać następująco: "127.0.0.1:8000/admin". </li>
      <li>Należy wykonać migracje komendą:"python .\manage.py makemigrations", a następnie "python .\manage.py migrate".</li>
    </ol>
  <li>Odpalenie zdokeryzowanej strony typu deploy(w przypadku systemu Linux)</li>
    <ol>
      <li>W terminalu należy wpisać komendę: "docker pull theripson/djangoproject:deploy"</li>
      <li>Następnie wpisanie komendy: "docker-compose.exe up".</li>
      <li>Serwer działa na IP Dockera. </li>
    </ol>
  <li>Wpisanie w przeglądarkę IP: "http://91.145.130.184"</li>
</ul>
<h2>Wykorzystane biblioteki</h2>
<ol>
  <li>Requests - obsługa API,</li>
  <li>Folium - generowanie i obsługa mapy,</li>
  <li>Reportlab - tworzenie PDF,</li>
  <li>Pillow - obsługa zdjęć,</li>
</ol>
<h1 align="center">FindTravel<br></h1>
<p align="center">Strona stworzona do tworzenia tras zwiedzania różnych atrakcji rozmieszczonych w całej Polsce!</p>
<img src="https://user-images.githubusercontent.com/100869542/174655743-d1206cd0-e7e0-474c-8378-9cf5cf7ec6b0.png"></img>
<p align="center">Potencjalny turysta na początku musi wybrać miasto do którego chciałby się wybrać.</p><br>
<img src="https://user-images.githubusercontent.com/100869542/174656097-a2013ca2-b877-4b2a-9f90-251c223cabd8.png"></img>
<p align="center">Po kliknięciu automatycznie zostanie przeniesiony do strony zawierającej wszystkie, możliwe atrakcje w wybranym mieście. Jeśli nie ma pomysłu na trasę może zdecydować się na gotową, stworzoną przez nasz zespół trasę.</p>
<img src="https://user-images.githubusercontent.com/100869542/174656425-d77bce73-7a7f-434c-9579-26fde9e369c4.png"></img>
<p align="center">Każda atrakcja ma swoje wspołrzędne, czas potrzebny na jej zwiedzanie, ewentualną cenę biletu wstępu i inne parametr</p>
<img src="https://user-images.githubusercontent.com/100869542/174657020-f815702d-1681-482d-a775-c2577aa2f049.png"></img>
<p align="center">Aby zacząć podróż wymagane jest zalogowanie się na stronie, użytkownik nieposiadający konta musi zarejestrować się. Aby użytkownik mógł dodać do planu atrakcję musi kliknąć na link "Dodaj do planu". Następnie może dowolnie dobierać sobie trasę.</p>
<img src="https://user-images.githubusercontent.com/100869542/174658707-019b413b-04f7-4c03-97c5-06af63e7f59a.png"></img>
<p align="center">Tak wygląda wybrana trasa na mapie, można ustawić też z którego punktu chcemy zacząć, a na którym skończyć, po kliknięciu przycisku "Zakończ" w profilu turysty pojawi się trasa, którą sobie zaplanował. W profilu może pobrać plik PDF swojej trasę, jeśli chce ją sobie wdrukować i mieć zawsze pod ręką!</p>

