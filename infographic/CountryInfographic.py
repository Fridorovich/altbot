import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
from PIL import Image
import numpy as np
import os
import re


class CountryInfographic:
    def __init__(self, data_file, flags_folder, country_name):
        """
        Инициализация класса для создания инфографики стран

        Args:
            data_file (str): путь к файлу со статистикой
            flags_folder (str): путь к папке с флагами
            country_name (str): название страны для парсинга
        """
        self.data_file = data_file
        self.flags_folder = flags_folder
        self.country_name = country_name
        self.country_data = {}
        self.load_data()

    def load_data(self):
        """Загрузка данных из файла статистики для конкретной страны"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as file:
                content = file.read()
                self.parse_country_data(content)
        except FileNotFoundError:
            print(f"Файл {self.data_file} не найден")
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")

    def parse_country_data(self, content):
        """Парсинг данных для конкретной страны"""
        country_pattern = rf"1\)\s*{re.escape(self.country_name)}"
        match = re.search(country_pattern, content)

        if not match:
            print(f"Данные для страны '{self.country_name}' не найдены")
            return

        start_idx = match.start()

        next_country_match = re.search(r"\n1\)\s*[^\n]", content[start_idx + 1:])
        if next_country_match:
            end_idx = start_idx + next_country_match.start() + 1
        else:
            end_idx = len(content)

        country_content = content[start_idx:end_idx]

        self.parse_country_sections(country_content)

    def parse_country_sections(self, content):
        """Парсинг всех секций данных страны"""
        # Извлекаем название страны
        name_match = re.search(r"1\)\s*(.+)", content)
        if name_match:
            self.country_data['name'] = name_match.group(1).strip()

        capital_match = re.search(r"14\)\s*[^:]*:\s*([^,\n]+)", content)
        if capital_match:
            self.country_data['capital'] = capital_match.group(1).strip()

        government_data = self.parse_government_data(content)
        self.country_data['government'] = government_data

        language_data = self.parse_language_data(content)
        self.country_data['language'] = language_data

        economy_type_data = self.parse_economy_type(content)
        self.country_data['economy_type'] = economy_type_data

        economy_match = re.search(r"8\)\s*(.+)", content)
        if economy_match:
            economy_data = self.parse_economy_structure(economy_match.group(1))
            self.country_data['economy_structure'] = economy_data

        export_data = self.parse_trade_data(content, 'экспорт')
        self.country_data['exports'] = export_data

        import_data = self.parse_trade_data(content, 'импорт')
        self.country_data['imports'] = import_data

        debt_data = self.parse_debt_data(content)
        self.country_data['debt'] = debt_data

        population_data = self.parse_population_data(content)
        self.country_data['population'] = population_data

    def parse_government_data(self, content):
        """Парсинг данных о форме правления из пункта 3"""
        government_match = re.search(r"3\)\s*(.+?)(?=\n\d+\)|\n*$)", content, re.DOTALL)
        if government_match:
            government_line = government_match.group(1).strip()
            if '.' in government_line:
                government_text = government_line.split('.')[0].strip()
                return government_text
            return government_line
        return 'Не указана'

    def parse_language_data(self, content):
        """Парсинг данных о языке из пункта 7"""
        language_match = re.search(r"7\)\s*(.+?)(?=\n\d+\)|\n*$)", content, re.DOTALL)
        if language_match:
            language_line = language_match.group(1).strip()
            if 'Государственный язык:' in language_line:
                lang_part = language_line.split('Государственный язык:')[1]
                if '.' in lang_part:
                    main_lang = lang_part.split('.')[0].strip()
                else:
                    main_lang = lang_part.strip()
                if '(' in main_lang:
                    main_lang = main_lang.split('(')[0].strip()
                if len(main_lang) > 20:
                    return "Слишком много\nдля отображения"
                return main_lang
            if '.' in language_line:
                if len(language_line) > 20:
                    return "Слишком много\nдля отображения"
                return language_line.split('.')[0].strip()
            if len(language_line) > 20:
                return "Слишком много\nдля отображения"
            return language_line
        return 'Не указан'

    def parse_economy_type(self, content):
        """Парсинг типа экономики из пункта 8"""
        economy_match = re.search(r"8\)\s*(.+?)(?=\n\d+\)|\n*$)", content, re.DOTALL)
        if economy_match:
            economy_line = economy_match.group(1).strip()
            if 'экономика:' in economy_line.lower():
                economy_type = economy_line.split(':')[0].strip()
                return economy_type
            elif 'экономика' in economy_line.lower():
                parts = re.split(r'экономика', economy_line, flags=re.IGNORECASE)
                if parts and parts[0]:
                    return parts[0].strip().rstrip(':')
            if '.' in economy_line:
                return economy_line.split('.')[0].strip()
            return economy_line
        return 'Не указан'

    def parse_economy_structure(self, economy_line):
        """Парсинг структуры экономики из пункта 8"""
        economy_data = {}

        patterns = [
            r'аграрный сектор\s*\((\d+)%\)',
            r'индустриальный сектор\s*\((\d+)%\)',
            r'постиндустриальный сектор\s*\((\d+)%\)'
        ]

        sectors = ['аграрный', 'индустриальный', 'постиндустриальный']

        for i, pattern in enumerate(patterns):
            match = re.search(pattern, economy_line.lower())
            if match:
                economy_data[sectors[i]] = int(match.group(1))

        if not economy_data:
            if 'аграрный' in economy_line.lower():
                agr_match = re.search(r'аграрный[^()]*\((\d+)', economy_line)
                if agr_match:
                    economy_data['аграрный'] = int(agr_match.group(1))

            if 'индустриальный' in economy_line.lower():
                ind_match = re.search(r'индустриальный[^()]*\((\d+)', economy_line)
                if ind_match:
                    economy_data['индустриальный'] = int(ind_match.group(1))

            if 'постиндустриальный' in economy_line.lower():
                post_match = re.search(r'постиндустриальный[^()]*\((\d+)', economy_line)
                if post_match:
                    economy_data['постиндустриальный'] = int(post_match.group(1))

        return economy_data

    def parse_trade_data(self, content, trade_type):
        """Парсинг данных об экспорте/импорте"""
        trade_data = {}

        if trade_type == 'экспорт':
            export_match = re.search(r"9\).*?Экспортируемые товары:(.*?)(?=Импортируемые товары:|\n\d+\)|\n*$)",
                                     content, re.DOTALL)
            if export_match:
                export_text = export_match.group(1)
                matches = re.findall(r'([^():]+)\s*\((\d+)%\)', export_text)
                for match in matches:
                    product = match[0].strip().rstrip(',')
                    percentage = int(match[1])
                    trade_data[product] = percentage

        elif trade_type == 'импорт':
            import_match = re.search(r"Импортируемые товары:(.*?)(?=\n\d+\)|\n*$)", content, re.DOTALL)
            if import_match:
                import_text = import_match.group(1)
                matches = re.findall(r'([^():]+)\s*\((\d+)%\)', import_text)
                for match in matches:
                    product = match[0].strip().rstrip(',')
                    percentage = int(match[1])
                    trade_data[product] = percentage

        return trade_data

    def parse_debt_data(self, content):
        """Парсинг данных о госдолге из пункта 10"""
        debt_data = {}

        debt_match = re.search(r"10\)\s*(.+?)(?=\n\d+\)|\n*$)", content, re.DOTALL)
        if debt_match:
            debt_line = debt_match.group(1)
            total_match = re.search(r'Общая задолженность.*?(\d+)%', debt_line)
            if total_match:
                debt_data['total'] = int(total_match.group(1))

            external_match = re.search(r'(\d+)% внешних', debt_line)
            if external_match:
                debt_data['external'] = int(external_match.group(1))

            internal_match = re.search(r'(\d+)% внутренних', debt_line)
            if internal_match:
                debt_data['internal'] = int(internal_match.group(1))

            population_match = re.search(r'(\d+)% займов у населения', debt_line)
            if population_match:
                debt_data['population'] = int(population_match.group(1))

        return debt_data

    def parse_population_data(self, content):
        """Парсинг данных о населении из пункта 15"""
        population_match = re.search(r"15\)\s*[^:]*:\s*([\d, ]+)", content)
        if population_match:
            population_text = population_match.group(1).strip()
            population_text = population_text.replace(' ', '').replace(',', '')
            try:
                return int(population_text)
            except ValueError:
                return population_text
        return 'Не указано'

    def create_infographic(self, output_path=None):
        """Создание инфографики для указанной страны"""
        if not self.country_data:
            print(f"Данные для страны '{self.country_name}' не загружены")
            return False

        if output_path is None:
            output_path = "infos/" + f"{self.country_name.lower()}_infographic.png"

        data = self.country_data

        fig = plt.figure(figsize=(14, 16))
        fig.patch.set_facecolor('#f0f0f0')

        gs = plt.GridSpec(4, 2, figure=fig, hspace=0.4, wspace=0.3)

        ax_title = fig.add_subplot(gs[0, :])
        ax_title.set_xlim(0, 1)
        ax_title.set_ylim(0, 1)
        ax_title.axis('off')

        title_box = FancyBboxPatch((0.1, 0.2), 0.8, 0.6,
                                   boxstyle="round,pad=0.1",
                                   linewidth=2,
                                   edgecolor='#2c3e50',
                                   facecolor='#34495e')
        ax_title.add_patch(title_box)

        ax_title.text(0.5, 0.7, data.get('name', self.country_name),
                      fontsize=24, fontweight='bold',
                      ha='center', va='center', color='white')
        ax_title.text(0.5, 0.3, 'ИНФОГРАФИКА',
                      fontsize=16, fontweight='normal',
                      ha='center', va='center', color='#ecf0f1')

        ax_flag = fig.add_subplot(gs[1, 0])
        ax_flag.axis('off')
        flag_path = os.path.join(self.flags_folder, "flags/" + f"{self.country_name.lower()}.png")

        if os.path.exists(flag_path):
            try:
                flag_img = Image.open(flag_path)
                ax_flag.imshow(flag_img)
                ax_flag.set_title('Флаг', fontsize=14, fontweight='bold', pad=10)
            except:
                self._create_flag_placeholder(ax_flag, self.country_name)
        else:
            self._create_flag_placeholder(ax_flag, self.country_name)

        ax_info = fig.add_subplot(gs[1, 1])
        ax_info.axis('off')

        info_text = f"Столица: {data.get('capital', 'Не указана')}\n"

        population = data.get('population', 'Не указано')
        if isinstance(population, int):
            info_text += f"Население: {population:,} чел.\n".replace(',', ' ')
        else:
            info_text += f"Население: {population}\n"

        government = data.get('government', 'Не указана')
        info_text += f"Форма правления: {government}\n"

        language = data.get('language', 'Не указан')
        info_text += f"Государственный язык: {language}"

        info_box = FancyBboxPatch((0.1, 0.1), 0.8, 0.8,
                                  boxstyle="round,pad=0.05",
                                  linewidth=1,
                                  edgecolor='#7f8c8d',
                                  facecolor='#ecf0f1')
        ax_info.add_patch(info_box)

        ax_info.text(0.5, 0.7, 'ОСНОВНАЯ ИНФОРМАЦИЯ',
                     fontsize=12, fontweight='bold',
                     ha='center', va='center', color='#2c3e50')
        ax_info.text(0.5, 0.4, info_text,
                     fontsize=10, ha='center', va='center',
                     color='#34495e', linespacing=1.5)

        ax_export = fig.add_subplot(gs[2, 0])
        ax_export.set_title('ТОП-5 ТОВАРОВ ЭКСПОРТА', fontsize=14, fontweight='bold', pad=20)

        exports = data.get('exports', {})
        if exports:
            top_exports = dict(sorted(exports.items(),
                                      key=lambda x: x[1], reverse=True)[:5])

            products = list(top_exports.keys())
            values = list(top_exports.values())

            bars = ax_export.bar(range(len(products)), values,
                                 color=plt.cm.Set3(np.linspace(0, 1, len(products))))

            for i, (bar, product, value) in enumerate(zip(bars, products, values)):
                height = bar.get_height()
                # Убираем запятые в названиях товаров
                clean_product = product.replace(',', '')
                ax_export.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                               f'{clean_product}\n{value}%',
                               ha='center', va='bottom', fontsize=9, fontweight='bold',
                               rotation=0, color='#2c3e50')

            ax_export.set_ylabel('Доля в экспорте (%)')
            ax_export.set_xticks([])
            ax_export.set_ylim(0, max(values) * 1.15)
            ax_export.grid(axis='y', alpha=0.3)
            ax_export.spines['top'].set_visible(False)
            ax_export.spines['right'].set_visible(False)
        else:
            ax_export.text(0.5, 0.5, 'Данные об экспорте\nнедоступны',
                           ha='center', va='center', fontsize=12,
                           transform=ax_export.transAxes)

        ax_import = fig.add_subplot(gs[2, 1])
        ax_import.set_title('ТОП-5 ТОВАРОВ ИМПОРТА', fontsize=14, fontweight='bold', pad=20)

        imports = data.get('imports', {})
        if imports:
            top_imports = dict(sorted(imports.items(),
                                      key=lambda x: x[1], reverse=True)[:5])

            products = list(top_imports.keys())
            values = list(top_imports.values())

            bars = ax_import.bar(range(len(products)), values,
                                 color=plt.cm.Pastel1(np.linspace(0, 1, len(products))))

            for i, (bar, product, value) in enumerate(zip(bars, products, values)):
                height = bar.get_height()
                clean_product = product.replace(',', '')
                ax_import.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                               f'{clean_product}\n{value}%',
                               ha='center', va='bottom', fontsize=9, fontweight='bold',
                               rotation=0, color='#2c3e50')

            ax_import.set_ylabel('Доля в импорте (%)')
            ax_import.set_xticks([])
            ax_import.set_ylim(0, max(values) * 1.15)
            ax_import.grid(axis='y', alpha=0.3)
            ax_import.spines['top'].set_visible(False)
            ax_import.spines['right'].set_visible(False)
        else:
            ax_import.text(0.5, 0.5, 'Данные об импорте\nнедоступны',
                           ha='center', va='center', fontsize=12,
                           transform=ax_import.transAxes)

        ax_economy = fig.add_subplot(gs[3, 0])
        ax_economy.axis('off')

        economy_structure = data.get('economy_structure', {})
        debt_data = data.get('debt', {})
        economy_type = data.get('economy_type', 'Не указан')

        economy_text = "ЭКОНОМИЧЕСКИЕ ПОКАЗАТЕЛИ\n\n"

        if economy_type != 'Не указан':
            economy_text += f"Тип экономики: {economy_type}\n"

        economy_text += "ВВП: данные уточняются\n"

        if 'total' in debt_data:
            economy_text += f"Госдолг: {debt_data['total']}% от ВВП\n"
        else:
            economy_text += "Госдолг: данные уточняются\n"

        if debt_data:
            if 'external' in debt_data:
                economy_text += f"Внешний долг: {debt_data['external']}%\n"
            if 'internal' in debt_data:
                economy_text += f"Внутренний долг: {debt_data['internal']}%\n"
            if 'population' in debt_data:
                economy_text += f"Займы у населения: {debt_data['population']}%"

        economy_box = FancyBboxPatch((0.1, 0.2), 0.8, 0.7,
                                     boxstyle="round,pad=0.05",
                                     linewidth=1,
                                     edgecolor='#27ae60',
                                     facecolor='#d5f4e6')
        ax_economy.add_patch(economy_box)

        ax_economy.text(0.5, 0.9, 'ЭКОНОМИКА',
                        fontsize=12, fontweight='bold',
                        ha='center', va='center', color='#27ae60')
        ax_economy.text(0.5, 0.5, economy_text,
                        fontsize=9, ha='center', va='center',
                        color='#2c3e50', linespacing=1.6)

        ax_structure = fig.add_subplot(gs[3, 1])

        if economy_structure:
            sector_display_names = {
                'аграрный': 'Аграрный',
                'индустриальный': 'Индустриальный',
                'постиндустриальный': 'Постиндустриальный'
            }

            sectors = []
            sizes = []
            colors = ['#27ae60', '#3498db', '#9b59b6']

            color_index = 0
            for sector_name, sector_value in economy_structure.items():
                if sector_value > 0:
                    display_name = sector_display_names.get(sector_name, sector_name.capitalize())
                    sectors.append(display_name)
                    sizes.append(sector_value)
                    color_index += 1

            if sectors and sum(sizes) > 0:
                display_colors = colors[:len(sectors)]

                wedges, texts, autotexts = ax_structure.pie(sizes, labels=sectors, colors=display_colors,
                                                            autopct='%1.1f%%', startangle=90)

                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')

                # ax_structure.legend(wedges, sectors, title="Сектора", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            else:
                ax_structure.text(0.5, 0.5, 'Данные о структуре\nэкономики недоступны',
                                  ha='center', va='center', fontsize=12)
        else:
            ax_structure.text(0.5, 0.5, 'Данные о структуре\nэкономики недоступны',
                              ha='center', va='center', fontsize=12)

        ax_structure.set_title('СЕКТОРА ЭКОНОМИКИ', fontsize=12, fontweight='bold', pad=20)

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#f0f0f0')
        plt.close()

        print(f"Инфографика для '{self.country_name}' сохранена как: {output_path}")

    def _create_flag_placeholder(self, ax, country_name):
        """Создание заглушки для флага"""
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.add_patch(plt.Rectangle((0.1, 0.1), 0.8, 0.8,
                                   facecolor='#bdc3c7', edgecolor='#7f8c8d'))
        ax.text(0.5, 0.5, 'ФЛАГ\nНЕ НАЙДЕН',
                ha='center', va='center', fontsize=10,
                fontweight='bold', color='#7f8c8d')
        ax.text(0.5, 0.2, country_name,
                ha='center', va='center', fontsize=8, color='#95a5a6')

    def get_country_data(self):
        """Получить данные по стране"""
        return self.country_data

    def print_parsed_data(self):
        """Вывести распарсенные данные для проверки"""
        print(f"\n=== Распарсенные данные для '{self.country_name}' ===")
        for key, value in self.country_data.items():
            print(f"{key}: {value}")


# Пример использования
if __name__ == "__main__":
    countries_to_process = ['Хаддген', 'Лаплата']

    for country in countries_to_process:
        print(f"\nОбработка страны: {country}")
        infographic = CountryInfographic('Статистика_1951.txt', 'flags', country)

        infographic.print_parsed_data()

        infographic.create_infographic()

