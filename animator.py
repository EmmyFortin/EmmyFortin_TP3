import random
import ui
from maya import cmds


def generate_random_animation(parameters, message):
    """Fonction qui créer l'animation random"""

    # Début de l'animation au keyframe 0
    first_keyframe = 0

    # Récupération de la valeur des paramètres duration et step
    duration = parameters["Animation Timing_Duration (Frames):"]
    step = parameters["Animation Timing_Step (Frames):"]

    # Récupère les objets sélectionnés
    objects = get_objects()

    # S'il n'y a pas d'objet sélectionné on appelle warning_message de ui.py
    if not objects:
        message("warning")
        return

    # Pour CTRL + Z, mets les modifications dans le même Undo
    cmds.undoInfo(openChunk=True, chunkName="Generate Random Animation")

    try:
        # Animation des objets
        cmds.currentTime(first_keyframe)
        # Plage d'animation
        cmds.playbackOptions(min=first_keyframe, max=duration)

        # Pour chaque objet sélectionné
        for object in objects:

            # Supprmier les anciens keyframes
            cmds.cutKey(
                object,
                attribute=["translate","rotate","scale"],
                clear=True
            )

            # Liste pour conserver les valeurs de départ du 1er keyframe
            first_keyframe_value = {}

            # On loop dans chaque new keyframe (ajouter à chaque step jusquà la fin de l'anim)
            for new_keyframe in range(first_keyframe, duration, step):
                # Loop dans chaque type de transformation puis dans chaque axe
                for transform in ["Translate", "Rotate", "Scale"]:
                    for axis in ["x", "y", "z"]:

                        # Récupère les valeurs min et max
                        # Concatène le nom du transform (Translate, Rotate ou Scale) avec Parameters_min(ou max) et l'axe
                        # Pour correpsondre au noms des paramètres définit pour les spinboxes (line 57)
                        min_value = parameters[f"{transform} Parameters_min {axis}:"]
                        max_value = parameters[f"{transform} Parameters_max {axis}:"]

                        # Détermine la valeur random entre min_value et max_value
                        keyframe_value = random.uniform(min_value, max_value)

                        # Modifier le nom de l'attribut afin qu'il correspond à celui dans Maya
                        # Donc nom va être : translateX
                        keyframe_attribute = f"{transform.lower()}{axis.upper()}"

                        # Conserve les valeurs du 1er keyframe
                        if new_keyframe == first_keyframe:
                            first_keyframe_value[keyframe_attribute] = keyframe_value

                        # Création du keyframe
                        cmds.setKeyframe(
                            object,
                            attribute=keyframe_attribute,
                            value=keyframe_value,
                            time=new_keyframe,
                        )

            # Donne les valeurs du 1er keyframe au dernier
            for keyframe_attribute, keyframe_value in first_keyframe_value.items():
                cmds.setKeyframe(
                    object,
                    attribute=keyframe_attribute,
                    value=keyframe_value,
                    time=duration,
                )

    finally:
        # Fin du Undo
        cmds.undoInfo(closeChunk=True)

    print(cmds.undoInfo(query=True, undoName=True))

    # Jouer l'animation (trouver comment bien looper)
    cmds.play(forward = True)

    #message("done")


def get_objects():
    """Fonction qui récupère les objets sélectionnés."""

    objects = cmds.ls(type="transform", selection=True)
    return objects
