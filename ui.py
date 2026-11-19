from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QGroupBox,
    QSpinBox,
    QMessageBox,
    QGridLayout,
)
from PySide6.QtCore import Qt
import animator


class RandomAnimatorGenerator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Random Animator Generator")
        self.setMinimumWidth(450)
        self.setMinimumHeight(750)
        self.create_ui()

    def create_parameter_group(self, parameter_group_title, parameter_names):
        """Fonction qui crée et configure un groupe de paramètres et ses paramètres dans le UI."""

        # Création d'un group_box qui contiendera les paramètres
        group_box = QGroupBox(parameter_group_title)

        # Place group_box dans le QGridLayout
        group_layout = QGridLayout(group_box)

        # Parcourt les paramètres pour créer leur labels et leur spinboxes
        for element, (name, values) in enumerate(parameter_names.items()):

            label = QLabel(name)
            spinbox = QSpinBox()

            # Donne une taille fixe au spinboxes
            spinbox.setFixedSize(65, 30)

            # Définit les valeurs max et min, 
            # selon le dictionnaire groups (ligne 107)
            spinbox.setRange(values[0], values[1])

            # Définit la valeur par défaut des spinboxes
            spinbox.setValue(values[2])

            # Définit le nombre de rangé et de colonnes
            row = element // 3
            col = element % 3

            # Place le label et la spinbox côte à côte 
            # dans une même cellule horizontal
            row_layout = QHBoxLayout()
            row_layout.addWidget(label)
            row_layout.addWidget(spinbox)
            group_layout.addLayout(row_layout, row, col, Qt.AlignCenter)

            # Création de la structure des noms des paramètres
            self.spinboxes[f"{parameter_group_title}_{name}"] = spinbox

        # La section Animation Timing a une plus petite group_box
        if parameter_group_title == "Animation Timing":
            group_box.setFixedHeight(100)

        return group_box

    def message(self, message_type):
        """Fonction qui permet d'avoir différent type de message."""

        if message_type == "warning":
            QMessageBox.warning(
                self,
                "WARNING",
                "Please select at least one object in the outliner."
            )

        elif message_type == "done":
            QMessageBox.information(
                self,
                "Animation Generated",
                "Animation generated successfully."
            )

    def send_parameters_value(self):
        """Fonction qui donne en paramètres les valeurs des paramètres des spinboxes et la fonction message au animator.py."""

        # Liste des parametres
        parameters = {}

        for name, spinbox in self.spinboxes.items():
            parameters[name] = spinbox.value()

        # Appelle la fonction generate random animation dans animator et lui passe la liste en parametres
        animator.generate_random_animation(parameters, self.message)

    def create_ui(self):
        """Fonction qui créer le UI."""

        layout = QGridLayout(self)

        # Création dictionnaire des spinbox
        self.spinboxes = {}

        # Dictionnaire des groups box
        # Donne les noms des groupes et des paramètres
        # Puis défini les valeur [Min, Max, Defaut]
        groups = {
            "Animation Timing": {
                "Duration (Frames):": [24, 1000, 100],
                "Step (Frames):": [1, 500, 30],
            },
            "Translate Parameters": {
                "min x:": [-1000, 1000, -5],
                "min y:": [-1000, 1000, -5],
                "min z:": [-1000, 1000, -5],
                "max x:": [-1000, 1000, 5],
                "max y:": [-1000, 1000, 5],
                "max z:": [-1000, 1000, 5],
            },
            "Rotate Parameters": {
                "min x:": [-360, 360, -180],
                "min y:": [-360, 360, -180],
                "min z:": [-360, 360, -180],
                "max x:": [-360, 360, 180],
                "max y:": [-360, 360, 180],
                "max z:": [-360, 360, 180],
            },
            "Scale Parameters": {
                "min x:": [1, 500, 1],
                "min y:": [1, 500, 1],
                "min z:": [1, 500, 1],
                "max x:": [1, 500, 2],
                "max y:": [1, 500, 2],
                "max z:": [1, 500, 2],
            },
        }

        for element, (parameter_group_title, names) in enumerate(groups.items()):
            group_box = self.create_parameter_group(parameter_group_title, names)
            layout.addWidget(group_box, element, 0)

        # Empeche le step de dépasser la duration
        duration = self.spinboxes["Animation Timing_Duration (Frames):"]
        step = self.spinboxes["Animation Timing_Step (Frames):"]
        duration.valueChanged.connect(step.setMaximum)
        step.setMaximum(duration.value())

        self.create_button = QPushButton("Generate")
        self.create_button.clicked.connect(self.send_parameters_value)

        layout.addWidget(self.create_button)
