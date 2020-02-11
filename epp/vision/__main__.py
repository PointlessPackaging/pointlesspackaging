from vision.consts import paths
from vision.api_calls import detect_labels


def main():
    # Labels detection
    for path in paths:
        print("=======================")
        detect_labels(paths)


if __name__ == "__main__":
    main()
