from sim.track import Track

# Select track
track = Track("sprites/track1.png")  # ou track2.png

# Inside game loop:
track.draw(screen)
car.draw(screen)

# Collision check
if track.check_collision(car.rect):
    print("Car went off the track!")
    running = False
