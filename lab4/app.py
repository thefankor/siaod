import sys
import math
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QInputDialog, QComboBox
)
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
from main import johnson  # Замените на актуальный путь к вашей реализации


class GraphEditor(QWidget):
    """
    Интерактивный редактор ориентированного графа с ручным вводом вершин и рёбер.
    Позволяет вычислить кратчайший путь алгоритмом Джонсона с визуализацией.
    """

    def __init__(self):
        """Инициализация окна и UI."""
        super().__init__()
        self.setWindowTitle("Ориентированный граф: ввод и визуализация")
        self.setGeometry(100, 100, 1000, 600)

        self.vertices = []      # Список координат вершин [(x, y), ...]
        self.edges = []         # Список рёбер (u, v, weight)
        self.adjacency = []     # Матрица смежности
        self.current_path = []  # Кратчайший путь (список вершин)
        self.start_vertex = None

        # Виджеты управления
        self.start_combo = QComboBox()
        self.end_combo = QComboBox()
        self.solve_button = QPushButton("Найти путь")
        self.solve_button.clicked.connect(self.solve)
        self.result_label = QLabel("")

        # Компоновка интерфейса
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Начальная вершина:"))
        right_layout.addWidget(self.start_combo)
        right_layout.addWidget(QLabel("Конечная вершина:"))
        right_layout.addWidget(self.end_combo)
        right_layout.addWidget(self.solve_button)
        right_layout.addWidget(self.result_label)
        right_layout.addStretch()

        main_layout = QHBoxLayout()
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

    def mousePressEvent(self, event):
        """Обработка клика мышью: создание вершин или рёбер."""
        if event.x() > 800:  # Игнорируем клик по UI
            return

        pos = event.pos()
        # Попытка соединить вершины
        for idx, (x, y) in enumerate(self.vertices):
            if (pos - QPoint(x, y)).manhattanLength() < 20:
                if self.start_vertex is None:
                    self.start_vertex = idx
                else:
                    end_vertex = idx
                    weight, ok = QInputDialog.getInt(self, "Вес ребра", f"{self.start_vertex} → {end_vertex}", 1)
                    if ok:
                        self.edges.append((self.start_vertex, end_vertex, weight))
                        self.adjacency[self.start_vertex][end_vertex] = weight
                    self.start_vertex = None
                self.update()
                return

        # Добавление новой вершины
        self.vertices.append((pos.x(), pos.y()))
        for row in self.adjacency:
            row.append(math.inf)
        self.adjacency.append([math.inf] * len(self.vertices))
        self.adjacency[-1][len(self.vertices) - 1] = 0

        self.start_combo.addItem(str(len(self.vertices) - 1))
        self.end_combo.addItem(str(len(self.vertices) - 1))
        self.update()

    def draw_arrow(self, painter, x1, y1, x2, y2, color=Qt.black, alpha=255):
        """
        Рисует стрелку от (x1, y1) к (x2, y2), учитывая радиус вершины.
        """
        qcolor = QColor(color)
        qcolor.setAlpha(alpha)
        painter.setPen(QPen(qcolor, 3))

        angle = math.atan2(y2 - y1, x2 - x1)
        radius = 10
        x2_adj = x2 - radius * math.cos(angle)
        y2_adj = y2 - radius * math.sin(angle)

        arrow_length = 15
        angle1 = angle + math.pi / 8
        angle2 = angle - math.pi / 8

        x3 = x2_adj - arrow_length * math.cos(angle1)
        y3 = y2_adj - arrow_length * math.sin(angle1)
        x4 = x2_adj - arrow_length * math.cos(angle2)
        y4 = y2_adj - arrow_length * math.sin(angle2)

        painter.drawLine(int(x2_adj), int(y2_adj), int(x3), int(y3))
        painter.drawLine(int(x2_adj), int(y2_adj), int(x4), int(y4))

    def draw_edge_label(self, painter, x1, y1, x2, y2, text):
        """
        Отображает метку веса ребра со смещением от середины линии.
        """
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2
        dx = x2 - x1
        dy = y2 - y1
        length = math.hypot(dx, dy)
        if length == 0:
            length = 1
        offset = 10
        nx = -dy / length
        ny = dx / length
        label_x = mx + offset * nx
        label_y = my + offset * ny
        painter.drawText(int(label_x), int(label_y), text)

    def paintEvent(self, event):
        """Рисует граф: вершины, рёбра, стрелки и веса."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        radius = 10

        # Путь
        if len(self.current_path) >= 2:
            transparent_red = QColor(255, 0, 0, 150)
            painter.setPen(QPen(transparent_red, 3))
            for i in range(len(self.current_path) - 1):
                u, v = self.current_path[i], self.current_path[i + 1]
                x1, y1 = self.vertices[u]
                x2, y2 = self.vertices[v]
                angle = math.atan2(y2 - y1, x2 - x1)
                x1_adj = x1 + radius * math.cos(angle)
                y1_adj = y1 + radius * math.sin(angle)
                x2_adj = x2 - radius * math.cos(angle)
                y2_adj = y2 - radius * math.sin(angle)
                painter.drawLine(int(x1_adj), int(y1_adj), int(x2_adj), int(y2_adj))
                self.draw_arrow(painter, x1, y1, x2, y2, color=Qt.red, alpha=150)

                for edge_u, edge_v, w in self.edges:
                    if edge_u == u and edge_v == v:
                        self.draw_edge_label(painter, x1, y1, x2, y2, str(w))
                        break

        # Остальные рёбра
        painter.setPen(QPen(Qt.black, 2))
        path_edges = set(zip(self.current_path, self.current_path[1:]))
        for u, v, w in self.edges:
            if (u, v) in path_edges:
                continue
            x1, y1 = self.vertices[u]
            x2, y2 = self.vertices[v]
            angle = math.atan2(y2 - y1, x2 - x1)
            x1_adj = x1 + radius * math.cos(angle)
            y1_adj = y1 + radius * math.sin(angle)
            x2_adj = x2 - radius * math.cos(angle)
            y2_adj = y2 - radius * math.sin(angle)
            painter.drawLine(int(x1_adj), int(y1_adj), int(x2_adj), int(y2_adj))
            self.draw_arrow(painter, x1, y1, x2, y2)
            self.draw_edge_label(painter, x1, y1, x2, y2, str(w))

        # Вершины
        for i, (x, y) in enumerate(self.vertices):
            painter.setBrush(Qt.white)
            painter.setPen(Qt.black)
            painter.drawEllipse(x - radius, y - radius, 2 * radius, 2 * radius)
            painter.drawText(x - 5, y + 5, str(i))

    def solve(self):
        """
        Обрабатывает нажатие кнопки 'Найти путь' — запускает алгоритм Джонсона.
        """
        if len(self.vertices) < 2:
            self.result_label.setText("Добавьте хотя бы 2 вершины")
            return

        start = int(self.start_combo.currentText())
        end = int(self.end_combo.currentText())

        try:
            result, path = johnson(self.adjacency, start, end)
            self.current_path = path
            if result is not None:
                self.result_label.setText(f"Путь из {start} в {end}: {result}")
            else:
                self.result_label.setText("Путь не найден")
        except Exception as e:
            self.result_label.setText(f"Ошибка: {str(e)}")

        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphEditor()
    window.show()
    sys.exit(app.exec_())
