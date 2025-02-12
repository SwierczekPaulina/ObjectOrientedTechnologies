from Vector2D import Vector2D
from Vector3DDecorator import Vector3DDecorator
from Vector3DInheritance import Vector3DInheritance
from Polar2DAdapter import Polar2DAdapter

def main():
    v1_2d = Vector2D(1, 2)
    v2_2d = Vector2D(3, 4)
    v3_2d = Vector2D(-1, -1)

    vectors_2d = [v1_2d, v2_2d, v3_2d]
    print("Testing 2D Vectors with Polar Adapter:")
    for v in vectors_2d:
        polar_adapter = Polar2DAdapter(v)
        print(f"Cartesian: {v.getComponents()}, Polar: {polar_adapter.getComponents()}")

    print("\nDot Product for all combinations (2D Vectors):")
    for i in range(len(vectors_2d)):
        for j in range(i + 1, len(vectors_2d)):
            dot_product = vectors_2d[i].cdot(vectors_2d[j])
            print(f"Dot Product of {vectors_2d[i].getComponents()} and {vectors_2d[j].getComponents()}: {dot_product}")

    print("\nCross Product (using decorator) for all combinations:")
    decorators = [Vector3DDecorator(v) for v in vectors_2d]
    for i in range(len(decorators)):
        for j in range(i + 1, len(decorators)):
            cross_product = decorators[i].cross(decorators[j])
            print(f"Cross Product of {vectors_2d[i].getComponents()} and {vectors_2d[j].getComponents()}: {cross_product.getComponents()}")

    v1_3d = Vector3DInheritance(1, 2, 3)
    v2_3d = Vector3DInheritance(4, 5, 6)
    v3_3d = Vector3DInheritance(-1, -2, -3)

    vectors_3d = [v1_3d, v2_3d, v3_3d]

    print("\nTesting 3D Vectors with Inheritance:")
    for v in vectors_3d:
        print(f"Vector Components: {v.getComponents()}, Magnitude: {v.abs()}")

    print("\nDot Product for all combinations (3D Vectors):")
    for i in range(len(vectors_3d)):
        for j in range(i + 1, len(vectors_3d)):
            dot_product = vectors_3d[i].cdot(vectors_3d[j])
            print(f"Dot Product of {vectors_3d[i].getComponents()} and {vectors_3d[j].getComponents()}: {dot_product}")

    print("\nCross Product (using inheritance) for all combinations:")
    for i in range(len(vectors_3d)):
        for j in range(i + 1, len(vectors_3d)):
            cross_product = vectors_3d[i].cross(vectors_3d[j])
            print(f"Cross Product of {vectors_3d[i].getComponents()} and {vectors_3d[j].getComponents()}: {cross_product.getComponents()}")

if __name__ == "__main__":
    main()