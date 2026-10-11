"""Zone d'intérêt : limite l'analyse utile à la piste et à ses abords.

La zone est un polygone en coordonnées normalisées (0..1) dans l'image, fourni par la
configuration ou par l'interface de mission. Un candidat est retenu si le milieu du bas
de son rectangle (point de contact au sol) est dans le polygone.
"""


class ZoneInteret:
    def __init__(self, polygone=None):
        # Sans polygone : toute l'image.
        self.polygone = [tuple(p) for p in polygone] if polygone else [(0, 0), (1, 0), (1, 1), (0, 1)]
        if len(self.polygone) < 3:
            raise ValueError("La zone d'intérêt doit avoir au moins 3 sommets")

    def contient_point(self, x, y):
        """Test du point dans le polygone (lancer de rayon), coordonnées normalisées."""
        dedans = False
        n = len(self.polygone)
        for i in range(n):
            x1, y1 = self.polygone[i]
            x2, y2 = self.polygone[(i + 1) % n]
            if (y1 > y) != (y2 > y):
                x_inter = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                if x < x_inter:
                    dedans = not dedans
        return dedans

    def contient(self, detection, largeur, hauteur):
        x1, y1, x2, y2 = detection.boite
        return self.contient_point((x1 + x2) / 2 / largeur, y2 / hauteur)

    def filtrer(self, detections, largeur, hauteur):
        return [d for d in detections if self.contient(d, largeur, hauteur)]

    def en_pixels(self, largeur, hauteur):
        return [(int(x * largeur), int(y * hauteur)) for x, y in self.polygone]
