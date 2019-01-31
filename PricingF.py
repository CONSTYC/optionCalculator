import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import datetime

'''
Author : CCCCC
'''


def BSMd1(K, F, sigma, r, T, q):
    d1 = (np.log(F/K) + (r - q + sigma**2/2) * T)/(sigma * T**0.5)
    return d1


def PricingBSM(K, F, sigma, r, T, q, OptionType):
    # 欧式 BSM
    d1 = BSMd1(K, F, sigma, r, T, q)
    d2 = d1 - sigma * (T**0.5)
    if OptionType.lower() == 'call':
        c = np.exp(-q * T) * F * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
        return c
    elif OptionType.lower() == 'put':
        p = np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * F * norm.cdf(-d1)
        return p
    elif OptionType.lower() == 'binary call':
        bc = np.exp(-r * T) * norm.cdf(d2)
        return bc
    elif OptionType.lower() == 'binary put':
        bp = np.exp(-r * T) * norm.cdf(-d2)
        return bp
    else:
        raise ValueError("Parameter OptionType Error")


def BSMDelta(K, F, sigma, r, T, q, OptionType):
    # 欧式 delta
    d1 = BSMd1(K, F, sigma, r, T, q)
    d2 = d1 - sigma * (T ** 0.5)
    if OptionType.lower() == 'call':
        return np.exp(-q * T) * norm.cdf(d1)
    elif OptionType.lower() == 'put':
        return np.exp(-q * T) * (norm.cdf(d1) - 1)
    elif OptionType.lower() == 'binary call':
        return np.exp(-r * T) * norm.pdf(d2) / (sigma * F * T**0.5)
    elif OptionType.lower() == 'binary put':
        return -np.exp(-r * T) * norm.pdf(d2) / (sigma * F * T**0.5)
    else:
        raise ValueError("parameter OptionType should either be 'call' or 'put'")


def BSMGamma(K, F, sigma, r, T, q):
    d1 = BSMd1(K, F, sigma, r, T, q)
    gamma = norm.pdf(d1) * np.exp(-q * T) / (F * sigma * T**0.5)
    return gamma


def BSMTheta(K, F, sigma, r, T, q, OptionType):
    d1 = BSMd1(K, F, sigma, r, T, q)
    d2 = d1 - sigma * (T ** 0.5)
    if OptionType.lower() == 'call':
        theta = -F * norm.pdf(d1) * sigma * np.exp(-q * T) / (2 * T**0.5) \
                + q * F * norm.cdf(d1) * np.exp(-q * T) - r * K * np.exp(-r * T) * norm.cdf(d2)
        return theta
    elif OptionType.lower() == 'put':
        theta = -F * norm.pdf(d1) * sigma * np.exp(-q * T) / (2 * T ** 0.5) \
                - q * F * norm.cdf(-d1) * np.exp(-q * T) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        return theta
    else:
        raise ValueError("parameter OptionType should either be 'call' or 'put'")


def BSMVega(K, F, sigma, r, T, q):
    d1 = BSMd1(K, F, sigma, r, T, q)
    vega = F * T**0.5 * norm.pdf(d1) * np.exp(-q * T)
    return vega


def PricingKV(K, F, sigma, r, T, q, OptionType):
    # 亚式看涨 KV
    q = q + sigma ** 2 / 6
    sigma = sigma / np.sqrt(3)
    d1 = BSMd1(K, F, sigma, r, T, q)
    d2 = d1 - sigma * (T**0.5)
    if OptionType.lower() == 'call':
        c = np.exp(-q * T) * F * norm.cdf(d1) - np.exp(-r * T) * K * norm.cdf(d2)
        return c
    elif OptionType.lower() == 'put':
        p = np.exp(-r * T) * K * norm.cdf(-d2) - np.exp(-q * T) * F * norm.cdf(-d1)
        return p
    else:
        raise ValueError("parameter OptionType should either be 'call' or 'put'")


def PricingBAW(K, F, sigma, r, T, q, OptionType, epsilon):
    n = 2 * (r - q) / (sigma**2)
    m = 2 * r / (sigma**2)
    k = 1 - np.exp(-r * T)
    q1 = (1 - n - np.sqrt((n - 1)**2 + 4 * m / k))/2
    q2 = (1 - n + np.sqrt((n - 1)**2 + 4 * m / k))/2

    dx = 0.01
    # epsilon = 0.00001
    i = 1
    imax = 50

    if OptionType.lower() == 'call':
        if q == 0:
            Call = PricingBSM(K, F, sigma, r, T, q, 'call')
        else:
            S1 = K
            while i <= imax:
                c0 = PricingBSM(K, S1, sigma, r, T, q, 'call')
                cu = PricingBSM(K, S1 * (1 + dx), sigma, r, T, q, 'call')
                cd = PricingBSM(K, S1 * (1 - dx), sigma, r, T, q, 'call')
                gap0 = S1 - K - c0 - (S1 / q2) * (1 - np.exp(-q * T) * norm.cdf(BSMd1(K, S1, sigma, r, T, q)))
                gapu = S1 * (1 + dx) - K - cu - (S1 * (1 + dx) / q2) * (
                    1 - np.exp(-q * T) * norm.cdf(BSMd1(K, S1 * (1 + dx), sigma, r, T, q)))
                gapd = S1 * (1 - dx) - K - cd - (S1 * (1 - dx) / q2) * (
                    1 - np.exp(-q * T) * norm.cdf(BSMd1(K, S1 * (1 - dx), sigma, r, T, q)))
                dfx = (gapu - gapd)/(2 * dx * S1)

                if np.abs(gap0 / K) <= epsilon:
                    break
                else:
                    S1 -= gap0/dfx
                    i += 1
            if F >= S1:
                Call = F - K
            else:
                bsmc = PricingBSM(K, F, sigma, r, T, q, 'call')
                Call = bsmc + (S1 / q2) * (
                    1 - np.exp(-q * T) * norm.cdf(BSMd1(K, S1, sigma, r, T, q))
                ) * (F / S1)**q2
        return Call

    elif OptionType.lower() == 'put':
        S2 = K
        while i <= imax:
            p0 = PricingBSM(K, S2, sigma, r, T, q, 'put')
            pu = PricingBSM(K, S2 * (1 + dx), sigma, r, T, q, 'put')
            pd = PricingBSM(K, S2 * (1 - dx), sigma, r, T, q, 'put')
            gap0 = K - S2 - p0 + (S2 / q1) * (1 - np.exp(-q * T) * norm.cdf(-BSMd1(K, S2, sigma, r, T, q)))
            gapu = K - S2 * (1 + dx) - pu + (S2 * (1 + dx) / q1) * (
                1 - np.exp(-q * T) * norm.cdf(-BSMd1(K, S2 * (1 + dx), sigma, r, T, q)))
            gapd = K - S2 * (1 - dx) - pd + (S2 * (1 - dx) / q1) * (
                1 - np.exp(-q * T) * norm.cdf(-BSMd1(K, S2 * (1 - dx), sigma, r, T, q)))
            dfx = (gapu - gapd)/(2 * dx * S2)
            if np.abs(gap0) <= epsilon:
                break
            else:
                S2 -= gap0/dfx
                i += 1
        if F <= S2:
            Put = K - F
        else:
            bsmp = PricingBSM(K, F, sigma, r, T, q, 'put')
            Put = bsmp - (S2 / q1) * (
                1 - np.exp(-q * T) * norm.cdf(-BSMd1(K, S2, sigma, r, T, q))
            ) * (F / S2)**q1
        return Put
    else:
        raise ValueError("parameter OptionType should either be 'call' or 'put'")


def BSMImpVol(K, F, sigma_guess, r, T, q, OptionType, opt):
    imax = 50
    i = 1
    epsilon = 0.00001
    while i <= imax:
        if np.abs(PricingBSM(K, F, sigma_guess, r, T, q, OptionType) - opt) <= epsilon:
            break
        else:
            sigma_guess -= (
                               PricingBSM(K, F, sigma_guess, r, T, q, OptionType) - opt
                           ) / BSMVega(K, F, sigma_guess, r, T, q)
            i += 1
    return sigma_guess


def BAWImpVol(K, F, sigma_guess, r, T, q, OptionType, epsilon, opt):
    imax = 200
    i = 0
    # epsilon = 0.00001
    dx = 0.0001
    while i <= imax:
        if np.abs(PricingBAW(K, F, sigma_guess, r, T, q, OptionType, epsilon) - opt) <= epsilon:
            break
        else:
            dfx = (
                PricingBAW(
                    K, F, sigma_guess * (1 + dx), r, T, q, OptionType, epsilon
                ) - PricingBAW(
                    K, F, sigma_guess * (1 - dx), r, T, q, OptionType, epsilon
                )
            ) / (2 * sigma_guess * dx)
            sigma_guess -= (
                               PricingBAW(K, F, sigma_guess, r, T, q, OptionType, epsilon) - opt
                           ) / dfx
            i += 1
    return sigma_guess


if __name__ == '__main__':
    Ts = np.array(range(1, 13)) / 12
    print(Ts)
    ds = BSMDelta(K=2.3, F=2.34, sigma=0.2, r=0.03, T=Ts, q=0, OptionType='put')

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.plot(Ts, ds)
    plt.show()
