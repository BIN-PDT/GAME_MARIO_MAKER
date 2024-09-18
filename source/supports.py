from os.path import join
from pygame.image import load


def import_image(*path, alpha=True, format="png"):
    full_path = f"{join(*path)}.{format}"
    surf = load(full_path)
    return surf.convert_alpha() if alpha else surf.convert()
