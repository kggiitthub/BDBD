import pandas as pd


def main():
    df = pd.read_csv('workspace/data/demo.csv')
    print('=== DataFrame (full) ===')
    print(df.to_string(index=False))
    print('\n=== Summary (info) ===')
    df.info()


if __name__ == '__main__':
    main()
