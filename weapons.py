import player


def fire_machine_gun(game, weapon_rect, weapon_level):
    if weapon_level == 1 or weapon_level == 3:
        bullet = player.Bullet(game, weapon_rect.centerx, weapon_rect.centery)
        game.player_bullets.add(bullet)
    if weapon_level == 2 or weapon_level == 3:
        bullet2 = player.Bullet(game, weapon_rect.centerx + 10, weapon_rect.centery)
        game.player_bullets.add(bullet2)
        bullet3 = player.Bullet(game, weapon_rect.centerx - 10, weapon_rect.centery)
        game.player_bullets.add(bullet3)
