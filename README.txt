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
	
	2.	Abra a aplicação CMD e navegue até à diretoria do projeto
	
	3.	Caso não tenha o projeto, utilize o comando “git clone https://github.com/Henr1ke/Stockshark.git” no CMD para fazer download do projeto para a diretoria
	
	4.	Instale as dependências do Python utilizando o comando “pip install -r requirements.txt” no CMD



Instalar e configurar o software ADB

	1.	Instalar o SDK command line tools:
	
		•	Aceda ao website https://developer.android.com/studio e faça download do zip que apenas contém as command line tools de SDK do Android. ATENÇÃO, não faça download da própria aplicação Android Studio, faça apenas download do zip com as command line tools. 
		
		•	Crie uma diretoria “Android_SDK” que irá conter o software ADB  e os AVDs. 
		
		•	Extraia o zip que acabou de fazer download para a diretoria “Android_SDK”
		
		•	Entre na diretoria “cmdline_tools” e crie uma nova diretoria com o nome “latest”
		
		•	Mova todos os ficheiros presentes na diretoria “cmdline_tools” para a diretoria “latest”
		
		•	Abra o CMD, navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin” e o comando “sdkmanager --help” para verificar que a instalação foi realizada com sucesso.


	2.	Instalar o package Platform-Tools:
	
		•	Abra o CMD, navegue até à diretoria “Android _SDK\cmdline-tools\latest\bin” e execute o comando “sdkmanager "platform-tools"” para instalar o ADB.
		
		•	Após ler os termos e condições, digite “y” para fazer downliad do package Platform-Tools na diretoria “Android_SDK”.
		

	3.	Configurar as variáveis de ambiente
		•	Na barra de pesquisas do Windows, pesquise por "Variáveis de ambiente". 
		
		•	Clique no botão "Variáveis de ambiente".
		
		•	Na seção "Variáveis do usuário", selecione a variável "Path" e clique em "Editar".
		
		•	Clique no botão “Novo” e coloque o caminho completo para a diretoria "platform-tools” presente dentro da diretoria “Android_SDK”.
		
		•	Clique em “OK” para guardar as alterações


	4.	Testar se está configurado corretamente
	
	•	Abra o CMD e execute o comando “adb version”.
	
	•	Se forem apresentadas as informações do ADB, então foi configurado corretamente
 



------------------------------------------------------------
						Utilização