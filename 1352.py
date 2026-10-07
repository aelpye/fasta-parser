class Seq:
    """
    Класс для работы с биологической последовательностью
    Хранит саму последовательность и информацию о ней (заголовок)
    Умеет красиво печататься в формате FASTA, считать длину и определять, белок это или нуклеотид
    """   
    def __init__(self, header, sequence):
        """
        Создаем новую последовательность
        
        header — это заголовок (мета-информация, название)
        sequence — это сама последовательность (буквы)
        """
        self.__header = header
        self.__sequence = sequence

#геттеры
    @property
    def header(self):
        """Возвращает заголовок последовательности"""
        return self.__header

    @property
    def sequence(self):
        """Возвращает саму последовательность"""
        return self.__sequence
#магические методы
    def __len__(self):
        """Возвращает длину последовательности (чтобы работала функция len())"""
        return len(self.__sequence)

    def __str__(self):
        """
        Красиво печатает последовательность в формате FASTA
        То есть сначала заголовок со знаком >, потом сама последовательность
        """
        return f">{self.__header}\n{self.__sequence}"

    def __repr__(self):
        """
        Техническое представление объекта (для отладки)
        Показывает заголовок и длину
        """
        return f"Seq(header='{self.__header}', length={len(self)})"
#свойство для определения типа последовательности
    @property 
    def alphabet(self):
        """
        Определяет, какой алфавит у последовательности: белковый или нуклеотидный
        Работает по стандарту IUPAC
        Возвращает 'protein', 'nucleotide' или 'unknown'
        """
        #множество букв, которые есть только в белках
        protein_only = set("EFILPQZJ")
        #множество всех букв, которые есть в нуклеотидах IUPAC
        nucleotide_IUPAC = set("ACGTURYSWKMBDHVN")
        #превращаем последовательность в множество уникальных букв
        seq_letters = set(self.__sequence)
        #если пересечение не пустое, есть буквы белков - это белок
        if seq_letters & protein_only:
            return "protein"
        #если все буквы есть входят в набор нуклеотидов IUPAC - это нуклеотид
        elif seq_letters <= nucleotide_IUPAC:
            return "nucleotide"
        #если ничего не подошло
        else:
            return "unknown"


class FastaReader:
    """
    Класс для чтения файлов в формате FASTA
    Проверяет, что файл действительно в формате FASTA, и читает его по записям 
    Использует генератор, чтобы не зависать на больших файлах
    """
    def __init__(self, filepath):
        """
        Создаем парсер для чтения FASTA-файлов
        
        filepath — это путь к файлу, который будем читать
        """
        self.__filepath = filepath    #сохранили путь

    def is_valid_fasta(self):
        """
        Проверяет, что файл действительно в формате FASTA
        Для этого смотрит, начинается ли первая непустая строка со знака >
        Возвращает True, если формат правильный, и False, если нет
        """
        with open(self.__filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                if line.startswith('>'):
                    return True
        return False 

    def parse(self):
        """
        Генератор, который читает файл по записям
        Находит заголовок (строка со знаком >), собирает последовательность и отдает готовый объект Seq
        
        Используется yield, чтобы не грузить весь файл в память сразу — это важно для больших файлов
        
        Если файл не в формате FASTA — выдает ошибку ValueError
        """
        #проверяем, что файл в нужном формате
        if not self.is_valid_fasta():
            raise ValueError("Файл не соответствует формату FASTA")

        #создаем переменные для хранения текущей записи
        header = None    #пока заголовка нет
        seq_chunks = []  #пока последовательность пустая

        with open(self.__filepath, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('>'):
                    if header is not None:
                        yield Seq(header, "".join(seq_chunks))
                    header = line[1:]
                    seq_chunks = []
                else:
                    seq_chunks.append(line)

        if header is not None:
            yield Seq(header, "".join(seq_chunks))



#Демонстрационная программа

if __name__ == "__main__":

    #1. Работа с классом Seq вручную
   
    print("Часть 1: Работа с классом Seq")
    
    # Создаем белок вручную
    protein = Seq("Инсулин человека", "MALWMRLLPLLALLALWGPDPAA")
    print(f"\n1. Белок:")
    print(f" Название: {protein.header}")
    print(f" Длина: {len(protein)}")
    print(f" Тип записи: {protein.alphabet}")
    
    #создаем нуклеотид вручную
    dna = Seq("Фрагмент ДНК", "ATGGCCCTGTGGATGCGT")
    print(f"\n2. Нуклеотид:")
    print(f" Название: {dna.header}")
    print(f" Длина: {len(dna)}")
    print(f" Тип записи: {dna.alphabet}")
    
    #красивый вывод через __str__
    print(f"\n3. Вывод через (__str__):")
    print(protein)
    
    #технический вывод через __repr__
    print(f"\n4. Технический вывод (__repr__):")
    print(repr(protein))
    print(repr(dna))


    
    #2. Работа с классом FastaReader

    print("\nЧасть 2: Работа с классом FastaReader")
    
    #создаем тестовый FASTA файл
    test_fasta = """>sp|P01308|INS_HUMAN Insulin OS=Homo sapiens
MALWMRLLPLLALLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPK
>gi|123456|ref|NM_001 Homo sapiens mRNA
ATGGCCCTGTGGATGCGTCTCCTGCCCCTGCTGCGCTGCTG
"""
    
    with open("test_sequences.fasta", "w", encoding="utf-8") as f:
        f.write(test_fasta)
    
    print("\nСоздан тестовый файл: test_sequences.fasta")
    
    #создаем парсер
    reader = FastaReader("test_sequences.fasta")
    
    #проверяем формат
    if reader.is_valid_fasta():
        print("Файл в формате FASTA\n")
    else:
        print("Файл не в формате FASTA")
    
    #читаем файл через генератор
    print("Читаем записи через генератор (yield) \n")
    for seq in reader.parse():
        print(repr(seq))
        print(f" Тип записи: {seq.alphabet}")
        print(f" Длина: {len(seq)}")
        print()



    #3. Работа с реальным файлом с UniProt

    print("Часть 3: Тест на реальном файле с UniProt")
    
    #создаем парсер для реального файла
    reader_uniprot = FastaReader("/home/user/Downloads/uniprot_test.fasta")
    
    #проверяем формат
    if reader_uniprot.is_valid_fasta():
        print("\n Файл uniprot_test.fasta в формате FASTA\n")
    else:
        print("\n Файл не в формате FASTA")
    
    #читаем файл через генератор
    print("Читаем 25 белков через генератор (yield) \n")
    for seq in reader_uniprot.parse():
        print(repr(seq))
        print(f" Тип записи: {seq.alphabet}")
        print(f" Длина: {len(seq)}")
        print()