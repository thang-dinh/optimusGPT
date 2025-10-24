import matplotlib.pyplot as plt

def visualize_tour(df, order):
    plt.figure(figsize=(6, 6))
    plt.title("Optimized TSP Tour")

    coords = df[['lat', 'lon']].values
    x, y = coords[:, 0], coords[:, 1]

    ordered_x = [x[i] for i in order]
    ordered_y = [y[i] for i in order]

    plt.plot(ordered_x, ordered_y, 'o-', color='blue')
    for i, label in enumerate(df['id']):
        plt.text(x[i]+0.02, y[i]+0.02, str(label))

    plt.show()
