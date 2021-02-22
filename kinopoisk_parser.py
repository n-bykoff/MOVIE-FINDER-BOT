import random
from selenium import webdriver
import time
import pickle


def write_pickle_to_file(data, name):
    with open(f'data/{name}.pickle', 'wb') as f:
        pickle.dump(data, f)


def read_pickle_file(file_name):
    with open(file_name, 'rb') as f:
        data = pickle.load(f)

    return data


def get_top_250_films():
    wd = webdriver.Chrome()
    descr_dic = {}

    for i in range(1, 6):

        wd.get(f'https://www.kinopoisk.ru/lists/top250/?page={i}&tab=all')
        film_hrefs = wd.find_elements_by_class_name('selection-film-item-meta__link')

        for i in range(len(film_hrefs)):
            film_hrefs[i] = film_hrefs[i].get_attribute('href')

        for href in film_hrefs:
            wd.get(href)
            time.sleep(2)

            film_name = wd.find_element_by_class_name('styles_title__2l0HH').text
            text = wd.find_element_by_class_name('styles_paragraph__2Otvx').text
            img = wd.find_element_by_class_name('film-poster').get_attribute('src')
            descr_dic[film_name] = [img, text]
            time.sleep(1)

    wd.close()
    write_pickle_to_file(descr_dic, 'main_data')


def random_film():
    data = read_pickle_file('data/main_data.pickle')

    index = random.randint(0, len(data))

    film_name = list(data.keys())[index]
    poster = data[film_name][0]
    description = data[film_name][1]

    return [film_name, poster, description]


if __name__ == '__main__':
    get_top_250_films()
