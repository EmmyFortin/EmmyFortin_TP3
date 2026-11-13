import random
import ui
from maya import cmds

def generate_random_animation(parameters):
    """Fonction qui créer l'animation random"""

    # Début de l'animation 
    first_keyframe = 0
    cmds.currentTime(first_keyframe)

    # Récupération de la valeur du parametre duration
    duration = parameters["Animation Timing_Duration (Frames):"]

    # Récupère la valeur de step
    step = parameters["Animation Timing_Step (Frames):"]

    # Plage d'animation
    cmds.playbackOptions(min=first_keyframe, max=duration)

    # Récupère les objets sélectionnés
    objects = get_objects()

    # Animation des objets

    # Pour chaque objet sélectionné
    for object in objects:
        # On loop dans chaque new keyframe (ajouter à chaque step jusquà la fin de l'anim)
        for new_keyframe in range(first_keyframe, duration + 1, step):
            # Loop dans chaque type de transformation puis dans chaque axe
            for transform in ["Translate", "Rotate", "Scale"]:
                for axis in ["x", "y", "z"]:

                    # Récupère les valeurs min et max
                    # Concatène le nom du transform (Translate, Rotate ou Scale) avec Parameters_min(ou max) et l'axe
                    # Pour correpsondre au noms des paramètres définit pour les spinboxes (line 57)
                    min_value = parameters[f"{transform} Parameters_min {axis}:"]
                    max_value = parameters[f"{transform} Parameters_max {axis}:"]

                    # Détermine la valeur random entre min_value et max_value
                    transformation_value = random.uniform(min_value, max_value)

                    # Modifier le nom de l'attribut afin qu'il correspond à celui dans Maya
                    # Donc nom va être : translateX
                    transformation_attribute = f"{transform.lower()}{axis.upper()}"

                    # Création du keyframe
                    cmds.setKeyframe(object, attribute=transformation_attribute, value=transformation_value, time=new_keyframe)

    # Jouer l'animation (trouver comment bien looper)
    cmds.play(forward = True)

def get_objects():
    """Fonction qui récupère les objets sélectionnés."""

    objects = cmds.ls(type="transform", selection=True)
    return objects

