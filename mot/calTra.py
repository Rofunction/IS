# coding: utf-8
import numpy as np
import math as m


def calTime(jm, am, vm, s1, s0, v0, v1):
    # 条件成立，达不到最大加速度
    if (vm - v0) * jm<pow(am, 2):
        Tj1 = m.sqrt((vm - v0) / jm)
        Ta = 2 * Tj1
    else:
        Tj1 = am / jm
        Ta = Tj1 + (vm - v0) / am
    # 判断是否存在最小加速度
    if (vm - v1) * jm<pow(am, 2):
        Tj2 = m.sqrt((vm - v1) / jm)
        Td = 2 * Tj2
    else:
        Tj2 = am / jm
        Td = Tj2 + (vm - v1) / am
    Tv = (s1 - s0) / vm - Ta / 2 * (1 + v0 / vm) - Td / 2 * (1 + v1 / vm)
    # 判断是否存在最大加速度
    if (Tv != 0):
        T = Ta + Tv + Td
    else:
        dalta = pow(am, 4) / pow(jm, 2) + 2 * (pow(v0, 2) + pow(v1, 2)) + am * (
                    4 * (s1 - s0) - 2 * (am / jm) * (v0 + v1))
        Ta = (pow(am, 2) / jm - 2 * v0 + m.sqrt(dalta)) / 2 * am
        Td = (pow(am, 2) / jm - 2 * v1 + m.sqrt(dalta)) / 2 * am
        T = Ta + Td
        # 判断能否达到最大，小加速度
        if (Ta<2 * am / jm) | (Td<2 * am / jm):
            return
    alim_a, alim_b = jm * Tj1, -jm * Tj2
    vlim = v0 + (Ta - Tj1) * alim_a
    timeIfom = np.array([Tj1, Tj2, Ta, Td, Tv, T, vlim, alim_a, alim_b])
    return timeIfom


def calTra(t, timeIfom, jm, s1, s0, v0, v1):

    Tj1, Tj2, Ta, Td, Tv = timeIfom[0], timeIfom[1], timeIfom[2], timeIfom[3], timeIfom[4]
    T, vlim, alim_a, alim_b = timeIfom[5], timeIfom[6], timeIfom[7], timeIfom[8]
    if 0<=t<=Tj1:
        p = (s0 + v0 * t + jm * pow(t, 3) / 6)*0<=t<=Tj1
        v = v0 + jm * pow(t, 3) / 2
        a = jm * t
    elif (Ta - Tj1)<=t<=Ta:
        p = s0 + (vlim + v0) * Ta / 2 - vlim * (Ta - t) + jm * pow(Ta - t, 3) / 6
        v = vlim - jm * pow(Ta - t, 2) / 2
        a = jm * (Ta - t)
    elif Ta<=t<=Ta + Tv:
        p = s0 + (vlim + v0) * Ta / 2 + vlim * (t - Ta)
        v = vlim
        a = 0
    elif (T - Td)<=t<=T - Td + Tj2:
        p = s1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) - jm * pow((t - T + Td), 3) / 6
        v = vlim - jm * pow(t - T + Td, 2) / 2
        a = -jm * (t - T + Td)
    elif (T - Td + Tj2)<=t<=T - Tj2:
        p = s1 - (vlim + v1) * Td / 2 + vlim * (t - T + Td) + alim_b * (
                    3 * pow(t - T + Td, 2) - 3 * Tj2 * (t - T + Td) + pow(Tj2, 2)) / 6
        v = vlim + alim_b * (t - T + Td - Tj2 / 2)
        a = alim_b
    elif (T - Tj2)<=t<=T:
        p = s1 - v1 * (T - t) - jm * pow(T - t, 3) / 6
        v = v1 + jm * pow(T - t, 2) / 2
        a = jm

    return p
