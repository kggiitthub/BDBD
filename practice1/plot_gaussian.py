#!/usr/bin/env python3
"""ガウス（正規）分布のグラフを描くスクリプト

使い方:
  - conda 環境を有効化して実行してください（例: `conda activate practice`）。
  - 実行: `python plot_gaussian.py`

出力:
  - 画面表示と `gaussian_plots.png` を作成します。
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, pi, exp


def normal_pdf(x, mu=0.0, sigma=1.0):
    coef = 1.0 / (sigma * sqrt(2.0 * pi))
    return coef * np.exp(-0.5 * ((x - mu) / sigma) ** 2)


def plot_pdfs(means, sigmas, x_range=None, save_path="gaussian_plots.png"):
    plt.figure(figsize=(8, 5))

    # 決め打ちの x 範囲がなければ、最初の組合せを元に作成
    if x_range is None:
        mu0 = means[0] if means else 0.0
        s0 = sigmas[0] if sigmas else 1.0
        x_min = mu0 - 4 * s0
        x_max = mu0 + 4 * s0
        # 幅を広げて他の sigma/mean も収まるようにする
        for mu, s in zip(means, sigmas):
            x_min = min(x_min, mu - 4 * s)
            x_max = max(x_max, mu + 4 * s)
        x = np.linspace(x_min, x_max, 1000)
    else:
        x = np.linspace(x_range[0], x_range[1], 1000)

    for mu, s in zip(means, sigmas):
        y = normal_pdf(x, mu, s)
        plt.plot(x, y, label=f"mu={mu}, sigma={s}")

    plt.title("Gaussian / Normal Distributions")
    plt.xlabel("x")
    plt.ylabel("pdf")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Saved plot to: {save_path}")
    plt.show()


def demo_hist_with_pdf(mu=0.0, sigma=1.0, n=2000):
    samples = np.random.normal(loc=mu, scale=sigma, size=n)
    plt.figure(figsize=(8, 5))
    # ヒストグラム（確率密度表示）
    plt.hist(samples, bins=50, density=True, alpha=0.6, color='C0', label='samples')
    # 理論的な PDF を重ねる
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    plt.plot(x, normal_pdf(x, mu, sigma), 'r-', lw=2, label=f'PDF mu={mu}, sigma={sigma}')
    plt.title('Histogram of samples with theoretical PDF')
    plt.xlabel('x')
    plt.ylabel('density')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('gaussian_hist.png')
    print('Saved histogram to: gaussian_hist.png')
    plt.show()


def main():
    p = argparse.ArgumentParser(description='Plot Gaussian/Normal distributions')
    p.add_argument('--means', nargs='+', type=float, default=[0.0, 2.0], help='list of means')
    p.add_argument('--sigmas', nargs='+', type=float, default=[1.0, 0.5], help='list of stddevs')
    p.add_argument('--hist', action='store_true', help='also draw histogram of samples for first mean/sigma')
    p.add_argument('--out', type=str, default='gaussian_plots.png', help='output png path')
    # Jupyter などで余分な引数が渡されることがあるため parse_known_args を使う
    args, _ = p.parse_known_args()

    # 入力長チェック
    if len(args.means) != len(args.sigmas):
        print('means と sigmas の数を合わせてください。')
        return

    plot_pdfs(args.means, args.sigmas, save_path=args.out)
    if args.hist:
        demo_hist_with_pdf(mu=args.means[0], sigma=args.sigmas[0])


if __name__ == '__main__':
    main()
