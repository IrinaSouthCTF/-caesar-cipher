import tkinter as tk
from tkinter import ttk, messagebox

# Алфавиты для шифра Цезаря
ALPHABETS = {
    "Русский": "абвгдеёжзийклмнопрстуфхцчшщъыьэюя",
    "English": "abcdefghijklmnopqrstuvwxyz",
}


def caesar_encrypt(text: str, key: int, alphabet: str):
    """Возвращает зашифрованный текст и двоичные номера его букв."""
    lower_alphabet = alphabet
    upper_alphabet = alphabet.upper()
    bits = len(alphabet).bit_length()
    encrypted = []
    binary_parts = []

    for char in text:
        if char in lower_alphabet:
            old_index = lower_alphabet.index(char)
            new_index = (old_index + key) % len(lower_alphabet)
            encrypted_char = lower_alphabet[new_index]
            encrypted.append(encrypted_char)
            binary_parts.append(format(new_index, f"0{bits}b"))
        elif char in upper_alphabet:
            old_index = upper_alphabet.index(char)
            new_index = (old_index + key) % len(upper_alphabet)
            encrypted_char = upper_alphabet[new_index]
            encrypted.append(encrypted_char)
            binary_parts.append(format(new_index, f"0{bits}b"))
        else:
            # Пробелы, цифры и знаки препинания не шифруются
            encrypted.append(char)
            binary_parts.append(char)

    return "".join(encrypted), " ".join(binary_parts)


def encrypt():
    text = input_text.get("1.0", "end-1c")
    key_value = key_entry.get().strip()

    if not text:
        messagebox.showwarning("Нет текста", "Введите исходное сообщение.")
        return

    try:
        key = int(key_value)
    except ValueError:
        messagebox.showerror("Ошибка ключа", "Ключ должен быть целым числом.")
        return

    alphabet_name = alphabet_box.get()
    alphabet = ALPHABETS[alphabet_name]

    encrypted_text, binary_text = caesar_encrypt(text, key, alphabet)

    encrypted_output.config(state="normal")
    encrypted_output.delete("1.0", "end")
    encrypted_output.insert("1.0", encrypted_text)
    encrypted_output.config(state="disabled")

    binary_output.config(state="normal")
    binary_output.delete("1.0", "end")
    binary_output.insert("1.0", binary_text)
    binary_output.config(state="disabled")

    count_label.config(text=f"Длина сообщения: {len(text)} символов")


def clear_all():
    input_text.delete("1.0", "end")
    key_entry.delete(0, "end")
    encrypted_output.config(state="normal")
    encrypted_output.delete("1.0", "end")
    encrypted_output.config(state="disabled")
    binary_output.config(state="normal")
    binary_output.delete("1.0", "end")
    binary_output.config(state="disabled")
    count_label.config(text="Длина сообщения: 0 символов")


root = tk.Tk()
root.title("Шифр Цезаря")
root.geometry("720x620")
root.minsize(620, 540)
root.configure(bg="#f2f4f8")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#f2f4f8", font=("Segoe UI", 10))
style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#20304a")
style.configure("TButton", font=("Segoe UI", 10), padding=8)
style.configure("TCombobox", padding=5)

main = ttk.Frame(root, padding=20)
main.pack(fill="both", expand=True)

ttk.Label(main, text="Шифр Цезаря", style="Header.TLabel").pack(anchor="w")
ttk.Label(
    main,
    text="Введите сообщение и целочисленный ключ. Отрицательный ключ выполняет сдвиг назад."
).pack(anchor="w", pady=(4, 14))

ttk.Label(main, text="Исходное сообщение (рекомендуется 20–30 символов):").pack(anchor="w")
input_text = tk.Text(main, height=4, wrap="word", font=("Consolas", 11), relief="solid", bd=1)
input_text.pack(fill="x", pady=(5, 4))
count_label = ttk.Label(main, text="Длина сообщения: 0 символов")
count_label.pack(anchor="e", pady=(0, 12))
input_text.bind("<KeyRelease>", lambda event: count_label.config(
    text=f"Длина сообщения: {len(input_text.get('1.0', 'end-1c'))} символов"
))

controls = ttk.Frame(main)
controls.pack(fill="x", pady=(0, 14))

ttk.Label(controls, text="Алфавит:").pack(side="left")
alphabet_box = ttk.Combobox(
    controls, values=list(ALPHABETS.keys()), state="readonly", width=12
)
alphabet_box.current(0)
alphabet_box.pack(side="left", padx=(7, 20))

ttk.Label(controls, text="Ключ (целое число):").pack(side="left")
key_entry = ttk.Entry(controls, width=12)
key_entry.insert(0, "3")
key_entry.pack(side="left", padx=7)

ttk.Button(controls, text="Зашифровать", command=encrypt).pack(side="left", padx=(8, 4))
ttk.Button(controls, text="Очистить", command=clear_all).pack(side="left", padx=4)

ttk.Label(main, text="Зашифрованное сообщение:").pack(anchor="w")
encrypted_output = tk.Text(main, height=3, wrap="word", font=("Consolas", 11), relief="solid", bd=1)
encrypted_output.pack(fill="x", pady=(5, 12))
encrypted_output.config(state="disabled")

ttk.Label(main, text="Двоичное представление номеров букв:").pack(anchor="w")
binary_output = tk.Text(main, height=5, wrap="word", font=("Consolas", 10), relief="solid", bd=1)
binary_output.pack(fill="both", expand=True, pady=(5, 8))
binary_output.config(state="disabled")

ttk.Label(
    main,
    text="Примечание: буквы нумеруются с нуля; для русского алфавита используются 6 бит, "
         "для английского — 5 бит. Пробелы и знаки препинания сохраняются.",
    wraplength=660,
    foreground="#53627a"
).pack(anchor="w", pady=(4, 0))

root.mainloop()
