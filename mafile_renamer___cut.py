import json
import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


APP_NAME = "mafile renamer + cut"
APP_VERSION = "1.0.0"
APP_AUTHOR = "smokov"


def safe_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name).strip()
    return name if name else "unknown"


def extract_values(file_path):
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            data = json.load(file)

        shared_secret = data.get("shared_secret", "")
        steam_id = str(data.get("Session", {}).get("SteamID", ""))
        account_name = data.get("account_name", "")

        if not shared_secret or not steam_id or not account_name:
            return None, "Нет одного из полей: shared_secret / Session.SteamID / account_name"

        return {
            "shared_secret": shared_secret,
            "Session": {
                "SteamID": steam_id,
            },
            "account_name": account_name,
        }, None
    except Exception as error:
        return None, str(error)


def log(message: str):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    root.update_idletasks()


def choose_folder():
    folder = filedialog.askdirectory(title="Выбери папку с .mafile")
    if folder:
        folder_var.set(folder)


def process_files():
    input_folder = folder_var.get().strip()

    if not input_folder:
        messagebox.showwarning("Ошибка", "Сначала выбери папку.")
        return

    if not os.path.isdir(input_folder):
        messagebox.showerror("Ошибка", "Указанная папка не существует.")
        return

    log_box.delete("1.0", tk.END)

    output_folder = os.path.join(input_folder, "ready")
    os.makedirs(output_folder, exist_ok=True)

    total = 0
    success = 0
    skipped = 0

    files = os.listdir(input_folder)
    mafiles = [filename for filename in files if filename.lower().endswith(".mafile")]

    if not mafiles:
        messagebox.showinfo("Информация", "В выбранной папке нет файлов .mafile")
        return

    log(f"Папка: {input_folder}")
    log(f"Папка результата: {output_folder}")
    log("-" * 50)

    for filename in mafiles:
        total += 1
        input_path = os.path.join(input_folder, filename)

        result, error = extract_values(input_path)
        if result is None:
            skipped += 1
            log(f"[SKIP] {filename} -> {error}")
            continue

        account_name = safe_filename(result["account_name"])
        new_data = {
            "shared_secret": result["shared_secret"],
            "Session": {
                "SteamID": result["Session"]["SteamID"],
            },
        }

        output_path = os.path.join(output_folder, f"{account_name}.mafile")

        try:
            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(new_data, file, ensure_ascii=False, separators=(",", ":"))
            success += 1
            log(f"[OK] {filename} -> {account_name}.mafile")
        except Exception as error:
            skipped += 1
            log(f"[ERR] {filename} -> ошибка сохранения: {error}")

    log("-" * 50)
    log(f"Всего .mafile: {total}")
    log(f"Успешно: {success}")
    log(f"Пропущено/ошибок: {skipped}")

    messagebox.showinfo(
        "Готово",
        (
            "Обработка завершена.\n\n"
            f"Успешно: {success}\n"
            f"Пропущено: {skipped}\n\n"
            f"Результат:\n{output_folder}"
        ),
    )


root = tk.Tk()
root.title(f"{APP_NAME} v{APP_VERSION}")
root.geometry("760x520")
root.resizable(False, False)

folder_var = tk.StringVar()

title_label = tk.Label(root, text=APP_NAME, font=("Arial", 16, "bold"))
title_label.pack(pady=(10, 2))

credit_label = tk.Label(root, text=f"v{APP_VERSION} by {APP_AUTHOR}", font=("Arial", 9))
credit_label.pack()

frame = tk.Frame(root)
frame.pack(fill="x", padx=15, pady=5)

folder_entry = tk.Entry(frame, textvariable=folder_var, font=("Arial", 11))
folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=4)

browse_button = tk.Button(frame, text="Выбрать папку", command=choose_folder, width=18)
browse_button.pack(side="left")

process_button = tk.Button(root, text="Обработать", command=process_files, font=("Arial", 11, "bold"), width=20)
process_button.pack(pady=10)

log_box = scrolledtext.ScrolledText(root, width=90, height=24, font=("Consolas", 10))
log_box.pack(padx=15, pady=10, fill="both", expand=True)

root.mainloop()
