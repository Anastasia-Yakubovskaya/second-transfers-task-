class AdaptiveMap:
    """
    Словарь, меняющий внутреннюю структуру в зависимости от числа элементов:
    None -> одиночная пара -> массив на 5 элементов -> обычный dict.
    """

    def __init__(self):
        self.size = 0
        self.storage = None

    def put(self, key, value):
        # Если словарь пустой
        if self.size == 0:
            self.storage = [key, value]
            self.size = 1
            return

        # Один элемент
        if self.size == 1:
            if self.storage[0] == key:
                self.storage[1] = value
            else:
                first_item = self.storage
                self.storage = [None] * 5
                self.storage[0] = first_item
                self.storage[1] = [key, value]
                self.size = 2
            return

        # От 2 до 5 элементов (используем массив)
        if self.size <= 5:
            for i in range(self.size):
                if self.storage[i][0] == key:
                    self.storage[i][1] = value
                    return

            if self.size < 5:
                self.storage[self.size] = [key, value]
                self.size += 1
            else:
                # Переносим всё в обычный dict
                res_dict = {}
                for item in self.storage:
                    res_dict[item[0]] = item[1]
                res_dict[key] = value

                self.storage = res_dict
                self.size = 6
            return

        # Если уже храним в dict
        if key not in self.storage:
            self.size += 1
        self.storage[key] = value

    def contains_key(self, key):
        """Проверка наличия ключа в словаре."""
        if self.size == 0:
            return False

        if self.size == 1:
            return self.storage[0] == key

        if self.size <= 5:
            for i in range(self.size):
                if self.storage[i][0] == key:
                    return True
            return False

        return key in self.storage

    def get(self, key):
        """Получение значения по ключу или сброс KeyError."""
        if self.size == 0:
            raise KeyError(key)

        if self.size == 1:
            if self.storage[0] == key:
                return self.storage[1]
            raise KeyError(key)

        if self.size <= 5:
            for i in range(self.size):
                if self.storage[i][0] == key:
                    return self.storage[i][1]
            raise KeyError(key)

        if key in self.storage:
            return self.storage[key]

        raise KeyError(key)