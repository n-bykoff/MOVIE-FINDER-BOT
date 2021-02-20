import random
from selenium import webdriver
import time
import pickle


def write_to_file(data):
    with open('data.pickle', 'wb') as f:
        pickle.dump(data, f)


def get_top_250_films():
    all_films_list = []
    all_imgs_list = []

    wd = webdriver.Chrome()

    for i in range(1, 6):
        wd.get(f'https://www.kinopoisk.ru/lists/top250/?page={i}&tab=all')
        films = wd.find_elements_by_class_name('selection-film-item-meta__name')

        for el in films:
            all_films_list.append(el.text)

        imgs = wd.find_elements_by_class_name('selection-film-item-poster__image')

        for el in imgs:
            all_imgs_list.append(el.get_attribute('src'))

        time.sleep(1)

    data = {}
    for i in range(len(all_imgs_list)):
        data[all_films_list[i]] = all_imgs_list[i]

    wd.close()
    write_to_file(data)


def random_film():
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)

    index = random.randint(0, len(data))

    film_name = list(data.keys())[index]
    poster = data[film_name]

    return [film_name, poster]


if __name__ == '__main__':
    get_top_250_films()