gravitational_constant = 6.67408E-11


def calculate_force(rocket, objects1, objects2):
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
    for obj in objects1:
        if rocket == obj:
            continue
        r = ((rocket.rect.centerx - obj.rect.centerx) ** 2 + (rocket.rect.centery - obj.rect.centery) ** 2) ** 0.5
        r = max(r, obj.r)
        f = gravitational_constant * rocket.m * obj.m / r ** 2
        rocket.Fx = f * (obj.rect.centerx - rocket.rect.centerx) / r
        rocket.Fy = f * (obj.rect.centery - rocket.rect.centery) / r
    for obj in objects2:
        if rocket == obj:
            continue
        r = ((rocket.rect.centerx - obj.rect.centerx) ** 2 + (rocket.rect.centery - obj.rect.centery) ** 2) ** 0.5
        r = max(r, obj.r)
        f = gravitational_constant * rocket.m * obj.m / r ** 2
        rocket.Fx = f * (obj.rect.centerx - rocket.rect.centerx) / r
        rocket.Fy = f * (obj.rect.centery - rocket.rect.centery) / r
