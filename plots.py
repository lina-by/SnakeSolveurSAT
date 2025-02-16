import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation
from itertools import product
from typing import Callable


def create_snake_path(solution, T, N, variable: Callable, pommes=None):
    snake_path = []
    snake_len = 3
    pommes_mangees = 0
    nb_pommes = 0 if pommes is None else len(pommes)
    for t in range(T):
        for x, y in product(range(N), range(N)):
            if variable((x, y, t), typ="s") in solution:
                if t == 0:
                    snake_path.append([(x, y)])
                else:
                    if pommes and t > snake_len:
                        nb_pommes_actives = [
                            1
                            for pomme_id in range(nb_pommes)
                            if variable(
                                typ="p",
                                id=(pomme_id, t - snake_len - pommes_mangees + 1),
                            )
                            in solution
                        ]
                        pommes_mangees = nb_pommes - sum(nb_pommes_actives)

                    new_position = [(x, y)] + snake_path[-1]
                    snake_path.append(new_position[: snake_len + pommes_mangees])

    return snake_path


def visualize_snake(
    grid_size,
    snake_path,
    animation_name="solution_animation.gif",
    apple_positions=[],
    pommes_successives=False,
):
    fig, ax = plt.subplots()
    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)

    # Fond de couleur sombre
    ax.set_facecolor("#282c34")

    # Bordure de la grille
    border = patches.Rectangle(
        (0, 0),
        grid_size,
        grid_size,
        linewidth=3,
        edgecolor="black",
        facecolor="none",
        zorder=3,
    )
    ax.add_patch(border)

    # Gestion des pommes
    apple_dict = {}
    current_apple_index = [0]  # Utilisation d'une liste pour modification dans update()

    def reset_apples():
        """Réinitialise les pommes selon le mode choisi"""
        for apple in apple_dict.values():
            apple.remove()
        apple_dict.clear()

        if pommes_successives:
            # Activer uniquement la première pomme
            if apple_positions:
                pos = apple_positions[0]
                apple = plt.Circle(
                    (pos[0] + 0.5, pos[1] + 0.5), 0.3, color="red", zorder=1
                )
                apple_dict[pos] = apple
                ax.add_patch(apple)
            current_apple_index[0] = 0  # Réinitialiser l'index
        else:
            # Activer toutes les pommes dès le début
            for pos in apple_positions:
                apple = plt.Circle(
                    (pos[0] + 0.5, pos[1] + 0.5), 0.3, color="red", zorder=1
                )
                apple_dict[pos] = apple
                ax.add_patch(apple)

    reset_apples()

    # Corps du serpent
    snake_patches = []

    def update(frame):
        current_frame = frame % len(snake_path)
        if current_frame == 0:
            reset_apples()

        current_snake = snake_path[current_frame]

        # Ajuster la longueur du serpent
        while len(snake_patches) < len(current_snake):
            patch = patches.Rectangle(
                (0, 0), 1, 1, color="#61dafb", ec="black", lw=2, zorder=2
            )
            ax.add_patch(patch)
            snake_patches.append(patch)

        while len(snake_patches) > len(current_snake):
            patch = snake_patches.pop()
            patch.remove()

        # Mettre à jour la position du serpent
        for i, (patch, pos) in enumerate(zip(snake_patches, current_snake)):
            patch.set_xy(pos)
            patch.set_facecolor("yellow" if i == 0 else "#61dafb")

        # Gestion des pommes successives
        head_pos = current_snake[0]
        if head_pos in apple_dict:
            apple_dict[head_pos].remove()
            del apple_dict[head_pos]

            if pommes_successives and current_apple_index[0] + 1 < len(apple_positions):
                current_apple_index[0] += 1
                next_pos = apple_positions[current_apple_index[0]]
                apple = plt.Circle(
                    (next_pos[0] + 0.5, next_pos[1] + 0.5), 0.3, color="red", zorder=1
                )
                apple_dict[next_pos] = apple
                ax.add_patch(apple)

    anim = animation.FuncAnimation(
        fig, update, frames=len(snake_path), interval=300, repeat=True
    )

    anim.save(animation_name)
    return anim



if __name__ == "__main__":
    # Exemple d'utilisation
    grid_size = 10
    snake_path = [
        [(2, 4), (2, 3), (2, 2)],
        [(2, 5), (2, 4), (2, 3)],
        [(3, 5), (2, 5), (2, 4)],
        [(4, 5), (3, 5), (2, 5)],
        [(4, 6), (4, 5), (3, 5), (2, 5)],
        [(4, 7), (4, 6), (4, 5), (3, 5)],
        [(5, 7), (4, 7), (4, 6), (4, 5)],
    ]
    apple_positions = [(2, 5), (3, 2), (5, 7)]

    visualize_snake(
        grid_size, snake_path, apple_positions=apple_positions, pommes_successives=True
    )
