from get_class_return_item import get_class_return_item


class Iterator:
    def __init__(self, type_of_class: str) -> None:
        self.counter = 0
        self.type_of_class = type_of_class
        self.elem = []

    def __next__(self) -> str:
        path = get_class_return_item(self.type_of_class, self.elem)
        if path != None:
            self.counter += 1
            self.elem.append(path)
            return self.elem[self.counter - 1]
        else:
            raise StopIteration

    def __iter__(self):
        return self
