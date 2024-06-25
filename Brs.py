import re


class Subject:
    def __init__(self, name: str, total: str, general: str):
        self.name_subject = name
        self.total = total
        self.general = general
        self.heads = dict()

    def add_head(self, head: str) -> None:
        self.heads[head] = dict()

    def add_event(self, head: str, event: str) -> None:
        name, rank = self.get_name_and_rank(event)
        self.heads[head][name] = dict()
        self.heads[head][name]['str'] = event
        self.heads[head][name]['dict'] = rank

    @staticmethod
    def get_name_and_rank(event: str):
        name = re.search(r'(\D+)\d+', event).group(1).strip()
        rank = re.search(r'(\d+\.\d+)/\d+', event).group(1)
        return name, rank

    def __iter__(self):
        return iter(self.heads)

    def __str__(self):
        count_eq = 10
        s = f'{self.total}\n{self.general}\n'
        s += '=' * count_eq + '\n'
        for head in self.heads:
            s += f'{head}\n'
            for event_name in self.heads[head]:
                s += f'{self.heads[head][event_name]["str"]}\n'
            s += '\n'
        return s.strip()

    def __eq__(self, other):
        return (isinstance(other, type(self)) and
                self.__dict__ == other.__dict__)
