import os
import sys
from random import randint
from time import sleep

import openpyxl
import requests
from loguru import logger
from lxml import html as ht

MAX_ATTEMPTS = 5  # Максимальное количество попыток получения ответа от сервера
TIMEOUT = 30  # Максимальное время ожидания ответа от сервера

# Базовые заголовки запроса
headers = {
	"user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/112.0"
}
curr_dir = os.path.dirname(os.path.realpath(__file__))
# Удаляем базовый обработчик
logger.remove()
# Устанавливаем новый обработчик для вывода информационных сообщений в консоль (для детального разбора - DEBUG)
logger.add(sys.stdout, level="INFO")


def get_request(url):
	"""Получает текст ответа сервера

	:param str url: Ссылка на страницу
	:return: Текст ответа
	:rtype: str | None
	"""
	# На случай если с первого раза не удалось загрузить страницу(часто бывает при массовом сборе и многопоточности)
	for i in range(MAX_ATTEMPTS):
		try:
			logger.debug(f"<GET {i} {url}")
			# Отправляем запрос на сервер
			r = requests.get(url, headers=headers, timeout=TIMEOUT)
			# Вызываем исключение, если пришел ошибочный ответ
			r.raise_for_status()
			# Проверяем нужный нам статус код ответа
			if r.status_code == 200:
				# Возвращаем текст ответа
				return r.text
		except Exception as e:
			logger.debug(f"<GET {i} failed {url} {e}")


def _get_genres(doc):
	"""Получает ссылки на жанры со страницы

	:param ht.HtmlElement doc: Html документ
	:return: Список ссылок на жанры
	:rtype: list[str]
	"""
	# Находим ссылки на жанры(вынесено в отдельную функцию на случай фильтрации)
	items = doc.xpath("//div[@class='pisateli_category_content']/ul/li/a")
	return [item.get("href") for item in items]


def get_genre_urls():
	"""Получает ссылки на жанры

	:return: Список ссылок на жанры(включая под-жанры)
	:rtype: list[str]
	"""
	logger.info("Собираю ссылки на жанры книг")
	url = "https://knigogo.net/zhanryi/"
	# Получаем текст ответа
	txt = get_request(url)
	# Если None, значит страница не загрузилась несмотря на несколько попыток ее загрузки
	if txt is None:
		logger.warning("Не удалось получить жанры")
		return []
	# Формируем структуру для работы с html тегами
	doc = ht.document_fromstring(txt)
	genres = []
	# Получаем основные жанры
	urls = _get_genres(doc)
	# Удаляем украинские книги
	try:
		urls.remove("https://knigogo.net/zhanryi/ukrayinski-knigi/")
	except ValueError:
		# Если ссылки нет в списке
		pass
	# Проходим по всем ссылкам и добавляем в genres ту, в которой под-жанров больше нет
	while len(urls) > 0:
		url = urls[0]
		txt = get_request(url)
		if txt is None:
			logger.warning(f"Не удалось загрузить {url}")
			continue
		doc = ht.document_fromstring(txt)
		new_urls = _get_genres(doc)
		# Если под-жанров нет, сохраняем ссылку
		if len(new_urls) == 0:
			genres.append(url)
		else:
			# Добавляем новые ссылки на под-жанры
			urls += new_urls
		# Удаляем проверенную ссылку из массива
		del urls[0]
		# Делаем небольшую задержку между запросами(чтобы не положить сервер)
		sleep(randint(2, 5))
	logger.info(f"Успешно получено {len(genres)} ссылок на жанры")
	return genres


def get_book_urls(url):
	"""Сбор ссылок на книги по жанру

	:param str url: Ссылка на жанр
	:return: Список ссылок на книги
	:rtype: list[str]
	"""
	logger.info(f"Собираю ссылки на книги по жанру {url}")
	urls = []
	while url is not None:
		txt = get_request(url)
		if txt is None:
			logger.warning(f"Не удалось загрузить страницу {url}")
			url = None
			# Не делаем return, т.к. хотим увидеть в логе информацию о кол-ве книг в этой категории(logger.info в конце)
			continue
		doc = ht.document_fromstring(txt)
		# Ищем ссылки на книги
		items = doc.xpath("//a[@class='book_link']")
		urls += [item.get("href") for item in items]
		# Ищем ссылку на следующую страницу
		try:
			url = doc.xpath("//a[@class='next filter_link']")[0].get("href")
		except IndexError:
			url = None
		sleep(randint(1, 3))
	logger.info(f"Успешно получено {len(urls)} ссылок на книги")
	return urls


def parse_book(item):
	"""Сбор данных о книге

	:param dict item: Данные о книге
	"""
	txt = get_request(item["url"])
	doc = ht.document_fromstring(txt)
	try:
		item["title"] = doc.xpath(
			"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Название:')]/text()"
		)[0].split(":")[1].strip()
	except IndexError:
		logger.debug(f"Не удалось получить название книги {item['url']}")
	try:
		# Если автор указан ссылкой
		item["author"] = doc.xpath(
			"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Писатель:')]/a/text()"
		)[0].strip()
	except IndexError:
		# Если автор не один и указаны ссылкой
		tmp = doc.xpath("//ul[@class='lib_book_preview_list']/li[contains(text(), 'Писатели:')]/a/text()")
		item["author"] = ", ".join([t.strip() for t in tmp])
		# Если автор не один указан не ссылкой
		try:
			tmp = doc.xpath(
				"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Писатели:')]/text()"
			)[0].split(":")[1].split(",")
		except IndexError:
			# Если автор не указан ссылкой
			tmp = doc.xpath(
				"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Писатель:')]/text()"
			)[0].split(":")[1].split(",")
		if len(tmp) == 0:
			logger.debug(f"Не удалось получить автора книги {item['url']}")
	try:
		item["year"] = doc.xpath(
			"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Год:')]/text()"
		)[0].split(":")[1].strip()
	except IndexError:
		logger.debug(f"Не удалось получить год книги {item['url']}")
	# Если жанры указаны ссылкой
	tmp = doc.xpath("//ul[@class='lib_book_preview_list']/li[contains(text(), 'Жанры:')]/a/text()")
	if len(tmp) == 0:
		# Если жанр один и указан ссылкой
		tmp = doc.xpath("//ul[@class='lib_book_preview_list']/li[contains(text(), 'Жанр:')]/a/text()")
	if len(tmp) == 0:
		try:
			# Если жанры не указаны ссылкой
			tmp = doc.xpath(
				"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Жанры:')]/text()"
			)[0].split(":")[1].split(",")
		except IndexError:
			# Если жанр один и не указан ссылкой
			tmp = doc.xpath(
				"//ul[@class='lib_book_preview_list']/li[contains(text(), 'Жанр:')]/text()"
			)[0].split(":")[1].split(",")
	item["genres"] = [t.strip() for t in tmp]


def save(data):
	"""Сохраняет данные о книгах в excel

	:param list[dict] data: Данные о книгах
	"""
	# Создаем exel документ
	wb = openpyxl.Workbook()
	sheet = wb.active
	# Добавляем шапку таблицы
	sheet.append(["Link", "Book name", "Author name", "Year", "Genres"])
	# Проходим по книгам и добавляем данные в таблицу
	for book in data:
		sheet.append([
			             book.get("url"), book.get("title"), book.get("author"), book.get("year")
		             ] + book.get("genres", []))
	# Сохраняем файл data.xlsx в директории со скриптом
	wb.save(os.path.join(curr_dir, "data.xlsx"))


def parse():
	# Собираем ссылки на жанры
	genre_urls = get_genre_urls()
	data = []
	exist_urls = []
	# Проходим по собранным жанрам и получаем ссылки на книги
	for genre_url in genre_urls:
		book_urls = get_book_urls(genre_url)
		# Проверяем уникальность полученных ссылок
		for book_url in book_urls:
			if book_url not in exist_urls:
				data.append({"url": book_url})
				exist_urls.append(book_url)
	# Проходим по книгам и получаем необходимую информацию
	for book in data:
		parse_book(book)
	save(data)
	logger.info("Сбор данных завершен")


if __name__ == '__main__':
	parse()
