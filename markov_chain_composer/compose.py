import os
import re
import string
import random

from graph import Graph, Vertex

def get_words_from_text(text_path):
    with open(text_path, "r") as f:
        text = f.read()

        # remove [text] if using the music lyrics
        text = re.sub(r'\[(.+)\]', ' ', text)

        # Turn all whitespace into single spaces
        text = " ".join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))

    words = text.split()
    return words

def make_graph(words):
    g = Graph()

    previous_word = None

    for word in words:
        word_vertex = g.get_vertex(word)

        if previous_word:
            previous_word.increment_edge(word_vertex)

        previous_word = word_vertex

    g.generate_probability_mappings()
    return g

def compose(g, words, length=50):
    composition = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = g.get_next_word(word)

    return composition

def main(artist):
    # For texts
    # words = get_words_from_text("texts/hp_sorcerer_stone.txt")

    words = []
    # For song lyrics
    for song_file in os.listdir(f"songs/{artist}"):
        if song_file == ".DS_Store":
            continue
        song_words = get_words_from_text(f"songs/{artist}/{song_file}")
        words.extend(song_words)

    g = make_graph(words)

    composition = compose(g, words, 100)
    return " ".join(composition)

if __name__ == '__main__':
    print(main("taylor_swift"))