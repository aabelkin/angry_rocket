gravitational_constant = 6.67408E-11

def calculate_force(rocket, planets):
    rocket.Fx = rocket.Fy = 0
    for obj in planets:
        if rocket == obj:
            continue
        r = ((rocket.rect.x - obj.x)**2 + (rocket.rect.y - obj.y)**2)**0.5
        r = max(r, obj.r)
        F = gravitational_constant * rocket.m * obj.m / r ** 2
        rocket.Fx = F * (obj.x - rocket.rect.x) / r
        rocket.Fy = F * (obj.y - rocket.rect.y) / r
