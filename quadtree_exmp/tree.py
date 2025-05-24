import json
import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon


def check_overlap(new_polygon, polygons):
    """Yeni bir çokgenin mevcut çokgenlerle kesişip kesişmediğini kontrol eder."""
    for polygon in polygons:
        if not (
                new_polygon["x2"] < polygon["x1"] or new_polygon["x1"] > polygon["x2"] or
                new_polygon["y4"] < polygon["y1"] or new_polygon["y1"] > polygon["y4"]
        ):
            return True  # Çakışma var
    return False  # Çakışma yok


def generate_random_polygon(existing_polygons):
    """Üst üste gelmeyen rastgele bir dörtgen oluşturur."""
    while True:
        x1, y1 = random.randint(0, 5000), random.randint(0, 5000)
        width, height = random.randint(50, 1000), random.randint(50, 1000)

        x2, y2 = x1 + width, y1
        x3, y3 = x1 + width, y1 + height
        x4, y4 = x1, y1 + height

        new_polygon = {"x1": x1, "y1": y1, "x2": x2, "y2": y2, "x3": x3, "y3": y3, "x4": x4, "y4": y4}

        # Çakışma kontrolü
        if not check_overlap(new_polygon, existing_polygons):
            return new_polygon


# JSON verisini oluştur
data = {
    "boundary": {"x": 0, "y": 0, "width": 5000, "height": 5000},
    "capacity": 3,
    "polygons": []
}

# 50 tane çakışmasız dörtgen oluştur ve JSON verisine ekle
for _ in range(50):
    new_polygon = generate_random_polygon(data["polygons"])
    data["polygons"].append(new_polygon)

# JSON dosyasını kaydet
with open("quad_tree_data.json", "w") as file:
    json.dump(data, file, indent=4)

print("Çakışmasız JSON dosyası başarıyla oluşturuldu.")


# Çokgen sınıfı, dört köşeli bir çokgeni temsil ediyor
class Point:
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3
        self.x4, self.y4 = x4, y4

    @property
    def center(self):
        # Çokgenin merkez noktasını hesapla
        center_x = (self.x1 + self.x2 + self.x3 + self.x4) / 4
        center_y = (self.y1 + self.y2 + self.y3 + self.y4) / 4
        return center_x, center_y


# QuadTree sınıfı
class QuadTree:
    def __init__(self, boundary, capacity=3):
        self.boundary = boundary
        self.capacity = capacity
        self.polygons = []
        self.divided = False

    def subdivide(self):
        x, y, w, h = self.boundary
        # Alt dörtgenleri tanımla
        nw = (x, y, w / 2, h / 2)
        ne = (x + w / 2, y, w / 2, h / 2)
        sw = (x, y + h / 2, w / 2, h / 2)
        se = (x + w / 2, y + h / 2, w / 2, h / 2)

        self.northwest = QuadTree(nw, self.capacity)
        self.northeast = QuadTree(ne, self.capacity)
        self.southwest = QuadTree(sw, self.capacity)
        self.southeast = QuadTree(se, self.capacity)
        self.divided = True

    def insert(self, polygon):
        # Çokgenin merkezini al
        center_x, center_y = polygon.center
        x, y, w, h = self.boundary

        # Merkezin sınırlar içinde olup olmadığını kontrol et
        if not (x <= center_x < x + w and y <= center_y < y + h):
            return False

        # Kapasite dolmadıysa çokgeni ekle
        if len(self.polygons) < self.capacity:
            self.polygons.append(polygon)
            return True
        else:
            # Kapasite dolduysa böl ve alt bölgelere eklemeyi dene
            if not self.divided:
                self.subdivide()

            # Alt bölgelere eklemeye çalış
            if self.northwest.insert(polygon): return True
            if self.northeast.insert(polygon): return True
            if self.southwest.insert(polygon): return True
            if self.southeast.insert(polygon): return True

        return False

    def draw(self, ax):
        x, y, w, h = self.boundary
        ax.add_patch(Rectangle((x, y), w, h, fill=False, edgecolor='black', linestyle='--'))

        if self.divided:
            self.northwest.draw(ax)
            self.northeast.draw(ax)
            self.southwest.draw(ax)
            self.southeast.draw(ax)

        for polygon in self.polygons:
            coords = [(polygon.x1, polygon.y1), (polygon.x2, polygon.y2),
                      (polygon.x3, polygon.y3), (polygon.x4, polygon.y4)]
            poly = Polygon(coords, closed=True, edgecolor='red', fill=False, linewidth=1.5)
            ax.add_patch(poly)


# JSON verisinden QuadTree yükleme fonksiyonu
def load_data_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    boundary = (
        data["boundary"]["x"],
        data["boundary"]["y"],
        data["boundary"]["width"],
        data["boundary"]["height"]
    )
    capacity = data["capacity"]

    qt = QuadTree(boundary, capacity)

    for point_data in data["polygons"]:
        polygon = Point(point_data["x1"], point_data["y1"],
                        point_data["x2"], point_data["y2"],
                        point_data["x3"], point_data["y3"],
                        point_data["x4"], point_data["y4"])
        qt.insert(polygon)

    return qt


# Test ve görselleştirme
if __name__ == "__main__":
    qt = load_data_from_json("quad_tree_data.json")

    fig, ax = plt.subplots(figsize=(10, 10))
    qt.draw(ax)
    ax.set_xlim(0, 5000)
    ax.set_ylim(0, 5000)

    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
