============================================================
						STOCKSHARK
============================================================

O StockShark é um programa de computador que joga xadrez na aplicação de telemóvel "Chess.com" usando o software ADB para controlar o telemóvel. 
É possível jogar contra um amigo ou contra o computador do "Chess.com". 
É possível instruir o programa para abrir a aplicação "Chess.com" no telemóvel, navegar nos seus menus, iniciar um jogo e jogá-lo, ou, se a aplicação já estiver aberta e o jogo estiver iniciado, instruir para apenas jogar xadrez



------------------------------------------------------------
						Requisitos

Certifique-se de ter os seguintes requisitos antes de executar o StockShark CLI:
	• Instale uma versão de Python 3.x
	• Instale as dependências do Python (verifique o ficheiro requirements.txt)
	• Instale o software ABD
	• Um modelo de telemóvel da seguinte lista:
		- Google Pixel 4
		- Google Pixel 3 
		- Xiaomi Mi 8 lite
	• Caso utilize um telemóvel físico, ative a opção de “USB Debugging” nas definições. Se necessitar, pesquise na internet como configurar essa opção para o seu modelo de telemóvel.
	• Caso não tenha ou não queira utilizar um telemóvel físico Android, instale um AVD (Android Virtual Device) de um dos modelos mencionados
	• Instale a aplicação “Chess.com” no telemóvel através da PlayStore e 	crie uma conta de utilizador


	
------------------------------------------------------------
						Configuração
								
						
Instalar e configurar o projeto Stockshark

	1.	Crie uma diretoria dedicada onde irá guardar o projeto

	2.	Abra o CMD e navegue até à diretoria do projeto

	3.	Caso não tenha o projeto, utilize o comando “git clone https://github.com/Henr1ke/Stockshark.git” no CMD para fazer download do projeto para a diretoria

	4.	Instale as dependências do Python utilizando o comando “pip install -r requirements.txt” no CMD



Instalar e configurar o software ADB

	1.	Certifique-se que tem a versão 8 do java (ou superior) instalada

	2.	Instalar o package Command Line Tools do Android SDK:
		•	Crie uma diretoria “Android_SDK” que irá conter o software relacionado com o ADB.
		•	Aceda ao website https://developer.android.com/studio e faça download do zip que apenas contém as command line tools de SDK do Android. ATENÇÃO, não faça download da própria aplicação Android Studio, faça apenas download do zip com as command line tools. 
		•	Extraia o zip que acabou de fazer download para a diretoria “Android_SDK”.
		•	Entre na diretoria “cmdline_tools” e crie uma nova diretoria com o nome “latest”.
		•	Mova TODOS os ficheiros e restantes pastas presentes na diretoria “cmdline_tools” para a diretoria “latest”.

	3.	Instalar os restantes packages necessários:
		•	Abra o CMD e navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin”.
		•	Execute o comando “sdkmanager platform-tools emulator tools” para instalar estes três packages.
		•	Após ler os termos e condições, digite “y” para iniciar o download dos packages.
		•	Se os packages estiverem bem instalados então existirão diretorias com o nome de cada um dos packages instalados dentro da diretoria “Android_SDK” (para além de outras diretorias).

	4.	Configurar as variáveis de ambiente
		•	Na barra de pesquisas do Windows, pesquise por "Variáveis de ambiente". 
		•	Clique no botão "Variáveis de ambiente".
		•	Na seção "Variáveis de utilizador", clique no botão “Novo”, no nome da variável insira “ANDROID_SDK_ROOT” e no valor da variável coloque o caminho COMPLETO para a diretoria "Android_SDK”.
		•	Na seção "Variáveis de utilizador", selecione a variável "Path" e clique em "Editar".
		•	Clique no botão “Novo” e coloque o caminho COMPLETO para a diretoria "Android_SDK/platform-tools”.
		•	Clique no botão “Novo” e coloque o caminho completo para a diretoria "Android_SDK/emulator”.
		•	Clique no botão “Novo” e coloque o caminho completo para a diretoria "Android_SDK/tools”.
		•	Clique em “OK” para guardar as alterações.
		•	É necessário fechar a aplicação do CMD para que as alterações sejam reconhecidas.

	5.	Testar se está configurado corretamente
		•	Abra o CMD e execute o comando “adb version” ou “emulator --help”.
		•	Se ao executar os comandos não surgirem erros então os packages foram instalados corretamente.



Instalar e configurar o software ADB

	1.	Certifique-se que tem a versão 8 do java (ou superior) instalada

	2.	Instalar o package Command Line Tools do Android SDK:
		•	Crie uma diretoria “Android_SDK” que irá conter o software relacionado com o ADB. 
		•	Aceda ao website https://developer.android.com/studio e faça download do zip que apenas contém as command line tools de SDK do Android. ATENÇÃO, não faça download da própria aplicação Android Studio, faça apenas download do zip com as command line tools. 
		•	Extraia o zip que acabou de fazer download para a diretoria “Android_SDK”.
		•	Entre na diretoria “cmdline_tools” e crie uma nova diretoria com o nome “latest”.
		•	Mova TODOS os ficheiros e restantes pastas presentes na diretoria “cmdline_tools” para a diretoria “latest”.

	3.	Instalar os restantes packages necessários:
		•	Abra o CMD e navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin”.
		•	Execute o comando “sdkmanager platform-tools emulator tools” para instalar estes três packages.
		•	Após ler os termos e condições, digite “y” para iniciar o download dos packages.
		•	Se os packages estiverem bem instalados então existirão diretorias com o nome de cada um dos packages instalados dentro da diretoria “Android_SDK” (para além de outras diretorias).

	4.	Configurar as variáveis de ambiente
		•	Na barra de pesquisas do Windows, pesquise por "Variáveis de ambiente".
		•	Clique no botão "Variáveis de ambiente".
		•	Na seção "Variáveis de utilizador", clique no botão “Novo”, no nome da variável insira “ANDROID_SDK_ROOT” e no valor da variável coloque o caminho COMPLETO para a diretoria "Android_SDK”.
		•	Na seção "Variáveis de utilizador", selecione a variável "Path" e clique em "Editar".
		•	Clique no botão “Novo” e coloque o caminho COMPLETO para a diretoria "Android_SDK/platform-tools”.
		•	Clique no botão “Novo” e coloque o caminho completo para a diretoria "Android_SDK/emulator”.
		•	Clique no botão “Novo” e coloque o caminho completo para a diretoria "Android_SDK/tools”.
		•	Clique em “OK” para guardar as alterações.
		•	É necessário fechar a aplicação do CMD para que as alterações sejam reconhecidas.

	5.	Testar se está configurado corretamente
		•	Abra o CMD e execute o comando “adb version” ou “emulator --help”.
		•	Se ao executar os comandos não surgirem erros então os packages foram instalados corretamente.



Instalar um modelo AVD

	1.	Instalar a versão do Android utilizada pelo AVD
		•	Abra o CMD e navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin”.
		•	Execute o comando “sdkmanager "platforms;android-30"” e seguidamente o comando “sdkmanager "system-images;android-30;google_apis_playstore;x86_64"” para obter a versão de android 30 que será utilizada pelo AVD.
		•	Após ler os termos e condições, digite “y” para iniciar download da versão do Android na diretoria “Android_SDK”.

	2.	Criar o modelo AVD
		•	Abra o CMD, navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin” e execute o comando “avdmanager create avd -n Pixel_4 -k "system-images;android-30;google_apis_playstore;x86_64" -d "pixel_4"” para criar o ADV do modelo Pixel 4.
		•	Por omissão o AVD é criado na diretoria “C:\Users\[Username]\.android”.

	3.	Testar se foi criado corretamente
		•	Abra o CMD e execute o comando “emulator -list-avds”.
		•	Se for apresentado o nome “Pixel_4” então o AVD foi configurado corretamente.

	4.	Configurar o modelo AVD
		•	Abra o ficheiro “C:\Users\[Username]\.android\avd\Pixel_4.avd\config.ini” num editor de texto e altere o valor do campo “hw.keyboard” para “yes”.

 

Iniciar o modelo AVD

	1.	Iniciar o AVD
		•	Abra o CMD.
		•	Execute o comando “adb start-server” para iniciar o software ADB.
		•	Execute o comando “emulator @Pixel_4 -port 5556” para iniciar o AVD.
		•	Aguarde que o emulador do AVD inicie.
		•	Se aparecer um pop-up a perguntar se pretende permitir o USB Debugging, permita.
		•	Se necessário, realize as configurações iniciais do modelo AVD.

	2.	Terminar o AVD
		•	Para terminar o AVD basta terminar o processo a decorrer no CMD utilizando as teclas “Ctrl+C”.



Instalar a aplicação chess.com

	1.	Instale a aplicação “Chess.com” disponível na PlayStore (https://play.google.com/store/apps/details?id=com.chess)

	2.	Crie uma conta de utilizador (Se quiser jogar contra amigos)

	3.	Vá ao separador “Mais” e aceda às definições

	4.	Clique no “Jogar” e seguidamente clique em “Partidas em Direto”

	5.	Ative a opção de “Dama automática”



------------------------------------------------------------
						Utilização
												
Para executar o programa do StockShark a partir da linha de comandos, abra o CMD e navegue até à diretoria "Stockshark/cli".

Para correr o programa Stockshark é necessário executar o código "python cli.py" seguido de vários outros paramêtros. Se tiver dúvidas sobre como utilizar o comando, pode sempre incluir "-h" na execução dos comandos para ser apresentado a informação de ajuda sobre o comando que está a tentar executar.




Os argumentos que se encontram entre parenteses retos são argumentos opcionais.
Os argumentos que se encontram entre chavetas são argumentos de escolha múltipla em que deve ser indicado apenas um dos elementos disponíveis na lista.
As reticências indicam partes do comando que estão a ser omitidas para simplificar o seu esclarecimento, mas que devem ser indicadas na sua execução


O comando base para correr o programa é o seguinte:

		python cli.py [-h] --engine {python_chess, stockshark} --agent {human, random, reactive, minmax} [--show_simulation] [navigate_menus ...] 
	
Argumentos:
	--engine: 
		Especifica o tipo de motor de xadrez a ser utilizado na simulação do jogo.
		Opções permitidas:
			* python_chess
			* stockshark
			
	--agent: 
		Especifica o tipo de agente que jogará xadrez.
		Opções permitidas:
			* human
			* random
			* reactive
			* minmax
			
	--show_simulation:
		Caso seja especificado, será apresentado na consola a simulação interna do jogo que está a ocorrer na aplicação "Chess.com"
	
	navigate_menus:
		É um comando opcional com sub-parâmetros que serão explicados de seguida. 
		Deve ser especificado caso se pretenda que o programa inicie a aplicação "Chess.com", navegue nos seus menus, inicie um jogo e jogue automaticamente.
		Caso não seja especificado, o programa apenas irá jogar o jogo de xadrez na aplicação "Chess.com". Neste caso, o programa não é responsável por navegar nos menus e iniciar um jogo, devendo o utilizador realizar essas tarefas.
		
		

O comando navigate_menus é o seguinte:

		python cli.py ... navigate_menus [-h] --model {pixel4, pixel3, mi8lite} {vs_friend ..., vs_computer ...} 
	
Argumentos:
	--model: 
		Especifica o modelo de telemóvel do AVD atual. Este parâmetro é necessário para uma correta navegação nos menus da aplicação.
		Opções permitidas:
			* pixel4
			* pixel3
			* mi8lite
	
	vs_friend:
		É um comando com sub-parâmetros que serão explicados de seguida. 
		Deve ser especificado caso se pretenda que o programa inicie um jogo contra um amigo.
		
	vs_computer:
		É um comando com sub-parâmetros que serão explicados de seguida. 
		Deve ser especificado caso se pretenda que o programa inicie um jogo contra o computador do "Chess.com".
		
		

O comando vs_friend é o seguinte:

		python cli.py ... navigate_menus ... vs_friend [-h] --username USERNAME [--play_as_whites | --play_as_blacks] [--timers_duration {1, 3, 5, 10, 30}]
	
Argumentos:
	--username: 
		Especifica o nome do utilizador "USERNAME" do amigo que se pretende desafiar num jogo de xadrez.
	
	--play_as_whites | --play_as_blacks:
		Apenas é possível especificar uma ou outra destas opções, mas não ambas simultaneamente. Caso alguma seja especificada o agente utilizará essa cor de peças, caso contrário a cor das peças será aleatória.
		
	--timers_duration:
		É um comando opcional que especifica a duração em minutos que cada jogador pode pensar durante toda a partida. O valor por omissão é 10. 
		Opções permitidas:
			* 1
			* 3
			* 5
			* 10
			* 30
			
			

O comando vs_computer é o seguinte:

		python cli.py ... navigate_menus ... vs_computer [-h] --diff_lvl {1, 2, 3, 4, 5} [--play_as_whites | --play_as_blacks]
	
Argumentos:
	--diff_lvl:
		Especifica o nível de dificuldade do computador da aplicação "Chess.com". 
		Opções permitidas:
			* 1
			* 2
			* 3
			* 4
			* 5
	
	--play_as_whites | --play_as_blacks:
		Apenas é possível especificar uma ou outra destas opções, mas não ambas simultaneamente. Caso alguma seja especificada o agente utilizará essa cor de peças, caso contrário a cor das peças será aleatória.
	