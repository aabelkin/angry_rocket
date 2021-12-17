gravitational_constant = 6.67408E-11

def calculate_force(rocket, objects):
    """Вычисляет силы, действующие на ракету rocket
    со стороны объектов objects

    Параметры
    ----------
    rocket : Sprite
        ракета
    objects : list
        объекты, действующие на ракету силой тяжести
    """
    rocket.Fx = rocket.Fy = 0
    for obj in objects:
        if rocket == obj:
            continue
        r = ((rocket.rect.centerx - obj.rect.centerx)**2 + (rocket.rect.centery - obj.rect.centery)**2)**0.5
        r = max(r, obj.r)
        F = gravitational_constant * rocket.m * obj.m / r ** 2
        rocket.Fx = F * (obj.rect.centerx - rocket.rect.centerx) / r
        rocket.Fy = F * (obj.rect.centery - rocket.rect.centery) / r
