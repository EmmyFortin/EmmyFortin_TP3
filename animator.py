import random
from maya import cmds


def generate_random_animation(parameters, message):
    """Fonction qui génère l'animation random."""

    # Début de l'animation au keyframe 0
    first_keyframe = 0

    # Récupération de la valeur des paramètres duration et step
    duration = parameters["Animation Timing_Duration (Frames):"]
    step = parameters["Animation Timing_Step (Frames):"]

    # Récupère les objets sélectionnés
    objects = get_objects()

    # S'il n'y a pas d'objet sélectionné,
    # on appelle la fonction message() avec
    # le type de message en paramètre de ui.py
    if not objects:
        message("warning")
        return

    # Pour CTRL + Z, met les modifications dans le même Undo
    cmds.undoInfo(openChunk=True, chunkName="Generate Random Animation")

    # Animation des objets
    try:
        cmds.currentTime(first_keyframe)

        # Plage d'animation
        cmds.playbackOptions(min=first_keyframe, max=duration)

        # Pour chaque objet sélectionné
        for object in objects:

            # Supprimer les anciens keyframes
            cmds.cutKey(
                object,
                attribute=["translate", "rotate", "scale"],
                clear=True
            )

            # Liste pour conserver les valeurs de départ du 1er keyframe
            first_keyframe_value = {}

            # On loop dans chaque nouveau keyframe
            # Les nouveau keyframes sont ajouter à chaque step
            for new_keyframe in range(first_keyframe, duration, step):

                # On loop dans chaque type de transformation,
                # puis dans chaque axe
                for transform in ["Translate", "Rotate", "Scale"]:
                    for axis in ["x", "y", "z"]:

                        # Récupère les valeurs min et max,
                        # selon la structure des noms
                        # définie dans ui.py (ligne 56)
                        min_value = parameters[
                            f"{transform} Parameters_min {axis}:"
                        ]
                        max_value = parameters[
                            f"{transform} Parameters_max {axis}:"
                        ]

                        # Détermine la valeur random
                        # entre min_value et max_value
                        keyframe_value = random.uniform(min_value, max_value)

                        # Modifier le nom de l'attribut afin
                        # qu'il corresponde à celui dans Maya (translateX)
                        keyframe_attribute = (
                            f"{transform.lower()}{axis.upper()}"
                        )

                        # Conserve les valeurs du 1er keyframe
                        if new_keyframe == first_keyframe:
                            first_keyframe_value[
                                keyframe_attribute
                            ] = keyframe_value

                        # Création du keyframe
                        cmds.setKeyframe(
                            object,
                            attribute=keyframe_attribute,
                            value=keyframe_value,
                            time=new_keyframe,
                        )

            # Donne les valeurs du 1er keyframe au dernier
            for keyframe_attribute, keyframe_value in (
                first_keyframe_value.items()
            ):
                cmds.setKeyframe(
                    object,
                    attribute=keyframe_attribute,
                    value=keyframe_value,
                    time=duration,
                )

    finally:
        # Fin du Undo
        cmds.undoInfo(closeChunk=True)

    # Appelle le QMessageBox de type done
    message("done")

def get_objects():
    """Fonction qui récupère les objets sélectionnés."""
    objects = cmds.ls(type="transform", selection=True)
    return objects
