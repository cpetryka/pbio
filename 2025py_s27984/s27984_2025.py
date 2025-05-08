# ====================================================================
# CEL PROGRAMU I KONTEKST:
# Program generuje losową sekwencję DNA (złożoną z nukleotydów A, C, G, T)
# oraz zapisuje ją do pliku w formacie FASTA. Program pobiera dane od
# użytkownika (długość sekwencji, ID, opis, imię), oblicza statystyki
# dotyczące zawartości nukleotydów oraz stosunek C+G do A+T.
# Imię użytkownika jest wstawiane w losowym miejscu sekwencji (jako "znacznik"),
# ale nie wpływa na statystyki ani długość sekwencji.
# ZASTOSOWANIE: edukacja bioinformatyczna, generowanie testowych sekwencji,
# demonstracja zapisu danych biologicznych w formacie FASTA.
# ====================================================================

import random  # import modułu do generowania liczb losowych
import re      # import modułu do wyrażeń regularnych (do walidacji ID)

# Funkcja generująca losową sekwencję DNA o zadanej długości
def generate_dna_sequence(length):
    return ''.join(random.choices('ACGT', k=length))  # losowy ciąg A, C, G, T

# Funkcja wstawiająca imię użytkownika w losowym miejscu sekwencji
def insert_name_into_sequence(sequence, name):
    position = random.randint(0, len(sequence))  # wybór pozycji wstawienia
    return sequence[:position] + name + sequence[position:]  # zwraca nową sekwencję

# Funkcja obliczająca statystyki (procentowa zawartość nukleotydów + %CG)
def calculate_statistics(sequence):
    # filtrujemy tylko prawdziwe nukleotydy (bez imienia użytkownika)
    dna_only = ''.join([nt for nt in sequence if nt in 'ACGT'])
    length = len(dna_only)
    stats = {nt: dna_only.count(nt) / length * 100 for nt in 'ACGT'}  # % zawartości
    cg = stats['C'] + stats['G']  # suma procentów C i G
    return stats, cg

# ORIGINAL:
# def save_to_fasta(filename, id_, description, sequence):
#     with open(filename, 'w') as f:
#         f.write(f">{id_} {description}\n")
#         f.write(sequence + '\n')

# MODIFIED (dzielenie sekwencji w pliku FASTA na linie po 60 znaków – standard FASTA):
def save_to_fasta(filename, id_, description, sequence):
    with open(filename, 'w') as f:
        f.write(f">{id_} {description}\n")  # nagłówek FASTA
        for i in range(0, len(sequence), 60):  # podział na linie
            f.write(sequence[i:i+60] + '\n')

# Główna funkcja programu
def main():
    try:
        length = int(input("Podaj długość sekwencji: "))  # pobranie długości
        if length <= 0:
            print("Długość musi być dodatnia.")  # walidacja
            return
    except ValueError:
        print("Podano nieprawidłową liczbę.")  # zabezpieczenie przed błędnym typem
        return

    # ORIGINAL:
    # seq_id = input("Podaj ID sekwencji: ").strip()
    # MODIFIED (walidacja ID – tylko litery, cyfry i podkreślenia):
    seq_id = input("Podaj ID sekwencji: ").strip()
    if not re.match(r'^\w+$', seq_id):  # tylko znaki bezpieczne dla nazw plików
        print("ID może zawierać tylko litery, cyfry i podkreślenia.")
        return

    description = input("Podaj opis sekwencji: ").strip()  # opis sekwencji
    name = input("Podaj imię: ").strip()  # imię do wstawienia

    dna_sequence = generate_dna_sequence(length)  # generowanie sekwencji
    final_sequence = insert_name_into_sequence(dna_sequence, name)  # wstawienie imienia
    stats, cg_ratio = calculate_statistics(final_sequence)  # obliczenie statystyk

    filename = f"{seq_id}.fasta"  # przygotowanie nazwy pliku
    save_to_fasta(filename, seq_id, description, final_sequence)  # zapis do pliku

    print(f"\nSekwencja została zapisana do pliku {filename}")  # komunikat dla użytkownika

    # MODIFIED (dodano wyświetlenie sekwencji – lepszy feedback):
    print("Wygenerowana sekwencja (z imieniem):")
    print(final_sequence)  # wyświetlenie sekwencji

    print("Statystyki sekwencji:")  # wyświetlenie statystyk
    for nt in 'ACGT':
        print(f"{nt}: {stats[nt]:.1f}%")
    print(f"%CG: {cg_ratio:.1f}")

# Uruchomienie programu (jeśli jest uruchamiany bezpośrednio)
if __name__ == "__main__":
    main()
