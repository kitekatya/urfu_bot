import HTTPGetter
import bs4
import re
from Brs import Subject


class Parser:
    def __init__(self, username, password):
        self.data = HTTPGetter.HTTPGetter().get_data(username, password)
        self.brs: dict[str] = dict()

    def parse(self):
        soup = bs4.BeautifulSoup(self.data, 'html.parser')
        brss = soup.findAll(class_='show')
        subjects = soup.findAll('a', class_='rating-discipline info-open')

        for subject, brs in zip(subjects, brss):
            total = self.get_rid_whitespaces(subject.text)
            general = self.parse_all_results(brs.find(class_='all-results').text)

            subj = Subject(subject['title'], total, general)
            self.brs[subject['title']] = subj

            containers = brs.findAll(class_='brs-marks-container')
            for container in containers:
                header = container.find(class_='brs-h4')
                subj.add_head(header['title'])
                coeffs_1 = float(header.find(class_='brs-gray').text)
                blocks = container.findAll(class_='brs-slide-pane-cont')
                for block in blocks:
                    coeffs_2 = float(block.find(class_='brs-gray').text)

                    events = block.findAll(class_='brs-values '
                                   'interim-certification')
                    for event in events:
                        s = self.parse_brs(event.text, round(coeffs_1 *
                                           coeffs_2, 4))
                        subj.add_event(header['title'], s)


    def parse_all_results(self, all_results):
        all_results = self.get_rid_whitespaces(all_results)
        all_results = all_results.replace('Общий', '\nОбщий')
        return all_results

    def parse_brs(self, string: str, coefficient: float):
        string = self.get_rid_whitespaces(string)
        lines = re.sub(r' из (\d+(.\d+)?)( )', r'/\1\n', string).split('\n')
        lines[-1] = lines[-1].replace(' из ', '/')

        for i in range(len(lines)):
            lines[i] = lines[i].capitalize()
            current = float(re.search('(\d+\.\d+)/\d+', lines[i]).group(1))
            lines[i] = '\t' + lines[i] + f' * {coefficient} = ' \
                                         f'{round(current * coefficient, 2)}'


        return '\n'.join(lines)

    def get_rid_whitespaces(self, string: str):
        return ' '.join(string.split())


