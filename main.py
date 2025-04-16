import os
import tkinter as tk
from tkinter import messagebox

from perceptron import Perceptron as Per1
from perceptron2 import Perceptron as Per2

def get_text_weights(text: str):
    fileweights = [0] * 26
    total = 0
    for char in text:
        if ord('a') <= ord(char.lower()) <= ord('z'):
            fileweights[ord(char.lower()) - ord('a')] += 1
            total+=1
    for i in range(len(fileweights)):
        fileweights[i] = float(fileweights[i] / total * 100)
    return fileweights

def read_all_files(data_dir):
    data = []
    for x in os.walk(data_dir):
        for filename in x[2]:
            fileweights = [0] * 26
            total = 0
            with open(os.path.join(x[0], filename), "r", encoding="utf8") as file:
                for char in file.read():
                    if ord('a') <= ord(char.lower()) <= ord('z') :
                        fileweights[ord(char.lower()) - ord('a')] += 1
                        total+=1
            for i in range(len(fileweights)):
                fileweights[i] = float(fileweights[i] / total * 100)
            data.append([x[0].split("\\")[1], fileweights])
    return data

def check_answer(perceptron, data):
    correctAnswer = 0
    needed = 0
    for language, inputs in data:
        if perceptron.calculate(inputs) == 1:
            correctAnswer += 1
        if language == perceptron.language:
            needed += 1
    return correctAnswer != needed

def main():
    first_perceptron_list = [Per1(26, 0.001, 0.001, x) for x in os.listdir("training_languages")]
    second_perceptron_list = [Per2(26, 0.001, x) for x in os.listdir("training_languages")]
    training_data = read_all_files("training_languages")
    test_data = read_all_files("test_languages")
    error_margin = 0.001
    max_epoque = 100

    print("Uczenie perceptronów pierwszej metody:\n")
    for perceptron in first_perceptron_list:
        epoque = 0
        while check_answer(perceptron, training_data) and epoque < max_epoque:
            epoque += 1
            for language, inputs in training_data:
                perceptron.learn(inputs, language == perceptron.language)
        print(f"Perceptron metody 1 języka {perceptron.language} uczył się {epoque} razy")

    print("\nUczenie perceptronu drugiej metody:\n")
    for perceptron in second_perceptron_list:
        epoque = 0
        to_break = 1
        while to_break and epoque < max_epoque:
            epoque += 1
            for language, inputs in training_data:
                if language != perceptron.language:
                    continue
                decision = 1 if language == perceptron.language else -1
                e = 0.5 * (decision - perceptron.calculate(inputs)) ** 2
                perceptron.learn(inputs, e)
                if e < error_margin:
                    to_break = 0
        print(f"Perceptron metody 2 języka {perceptron.language} uczył się {epoque} razy")
    print("\n\n")

    print("Wyniki dla pierwszego perceptronu z danych testowych")
    classified = 0
    for language, inputs in test_data:
        active_perceptrons = []
        for perceptron in first_perceptron_list:
            if perceptron.calculate(inputs) == 1:
                active_perceptrons.append(perceptron)
        if len(active_perceptrons) == 1:
            print(f"Tekst: {language}\tPercpetron: {active_perceptrons[0].language}\t{active_perceptrons[0].calculate(inputs)}")
            classified += 1
        else:
            print(f"Tekst: {language} nie został poprawnie zakwalifikowany")
    print(f"Dokładność klasyfikacji wynosi: {classified/len(test_data)*100}%\n")

    print("Wyniki dla drugiego perceptronu z danych testowych")
    classified = 0
    for language, inputs in test_data:
        output = []
        for perceptron in second_perceptron_list:
            output.append([perceptron.language, perceptron.calculate(inputs)])
        winner = max(output, key=lambda x: x[1])
        if language == winner[0]:
            classified += 1
        print(f"Text: {language} -> Predicted: {winner[0]} (score: {winner[1]:.6f})")
    print()
    print(f"Dokładność klasyfikacji wynosi: {classified/len(test_data)*100}%\n")
    print("\n\n")

    root = tk.Tk("Klasyfikator")
    root.geometry("400x250")

    label = tk.Label(root, text="Wpisz tekst do klasyfikacji")
    label.pack(pady=10)

    entry = tk.Text(root, width=50, height=7)
    entry.pack()

    result = tk.Label(root, text="", font=('Arial', 12))
    result.pack()

    def classify_text1():
        user_string = entry.get("1.0", tk.END).strip()
        if not user_string.strip():
            messagebox.showwarning("Błąd", "Wpisz coś do pola tekstowego")
            return
        weights = get_text_weights(user_string)
        classified = 0
        for per in first_perceptron_list:
            if per.calculate(weights) == 1:
                classified = 1
                result.config(text=f"Metoda 1 zakwalifikowano jako: {per.language} ")
        if not classified:
            result.config(text="Nie udało się zakwalifikować tekstu")

    def classify_text2():
        user_string = entry.get("1.0", tk.END).strip()
        if not user_string.strip():
            messagebox.showwarning("Błąd", "Wpisz coś do pola tekstowego")
            return

        output = []
        for per in second_perceptron_list:
            output.append([per.language, per.calculate(get_text_weights(user_string))])
        winner = max(output, key=lambda x: x[1])

        result.config(text=f"Metoda 2 zakwalifikowano jako: {winner[0]} (score: {winner[1]:.3f})")

    button1 = tk.Button(root, text="Klasyfikuj metodą 1", command=classify_text1)
    button1.pack(pady=1)
    button2 = tk.Button(root, text="Klasyfikuj metodą 2", command=classify_text2)
    button2.pack(pady=1)

    root.mainloop()

if __name__ == '__main__':
    main()