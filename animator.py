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

    # Récupération des valeurs des paramètres Translate, Rotate et Scale



    # Récupère les objets sélectionnés
    objects = get_objects()

    # Animation des objets
    for object in objects:
        # Ajoute un keyframe selon le step jusqu'à la fin de l'anim
        # + 1 car in range ignore la derniere valeur
        for frame in range(first_keyframe, duration + 1, step):
            cmds.setKeyframe(object, attribute= "translateX", value=frame, time=frame)

    # Jouer l'animation (trouver comment bien looper)
    cmds.play(forward = True)


        
def get_objects():
    """Fonction qui récupère les objets sélectionnés."""

    objects = cmds.ls(type="transform", selection=True)
    return objects

